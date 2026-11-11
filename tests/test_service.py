"""Tests against a real Etebase server that allows signups (e.g. the ciphwren-server test-server image).

The server is given in ETEBASE_TEST_API_URL. Install the package, then run from this directory (so
that the uncompiled source isn't imported instead): python -m unittest test_service
"""

import os
import unittest
import uuid

from etebase import Account, Client, FetchOptions, User

SERVER_URL = os.environ.get("ETEBASE_TEST_API_URL", "http://localhost:3735/")
COL_TYPE = "some.coltype"


class TestService(unittest.TestCase):
    def test_main(self):
        client = Client("python_test", SERVER_URL)

        self.assertTrue(Account.is_etebase_server(client))

        username = "py" + uuid.uuid4().hex[:10]
        password = "pw-" + uuid.uuid4().hex
        etebase = Account.signup(client, User(username, "test@example.com"), password)

        # A saved session can be restored
        etebase = Account.restore(client, etebase.save(None), None)
        etebase.fetch_token()

        col_mgr = etebase.get_collection_manager()
        col_meta = {"name": "Name"}
        col = col_mgr.create(COL_TYPE, col_meta, b"Something")
        col_meta["bloop"] = "blap"
        col.meta = col_meta
        self.assertEqual(b"Something", bytes(col.content))
        self.assertEqual(COL_TYPE, col.collection_type)

        fetch_options = FetchOptions().prefetch(True)
        col_mgr.upload(col, fetch_options)

        col_list = col_mgr.list(COL_TYPE, None)
        self.assertNotEqual(0, len(list(col_list.data)))
        fetch_options = FetchOptions().stoken(col_list.stoken)
        col_list = col_mgr.list(COL_TYPE, fetch_options)
        self.assertEqual(0, len(list(col_list.data)))

        col2 = col_mgr.fetch(col.uid, None)
        self.assertEqual(b"Something", bytes(col2.content))
        col2.content = b"Something else"
        col_mgr.transaction(col2, None)

        it_mgr = col_mgr.get_item_manager(col)
        item_meta = {"type": "Bla"}
        item = it_mgr.create(item_meta, b"Something item")
        item_meta = {"type": "Bla", "bloop": "blap"}
        item.meta = item_meta
        self.assertNotEqual("", item.uid)
        self.assertIsNotNone(item.etag)
        self.assertEqual(b"Something item", bytes(item.content))

        it_mgr.batch([item], None, None)
        etag1 = item.etag
        self.assertIsNotNone(etag1)
        item.content = b"Something item2"

        it_mgr.transaction([item], None, None)
        self.assertNotEqual(item.etag, etag1)

        item_list = it_mgr.list(None)
        self.assertEqual(1, len(list(item_list.data)))
        it_first = list(item_list.data)[0]
        self.assertEqual(b"Something item2", bytes(it_first.content))

        fetch_options = FetchOptions().stoken(item_list.stoken)
        item_list = it_mgr.list(fetch_options)
        self.assertEqual(0, len(list(item_list.data)))

        etebase.logout()

        # A new login gets everything back from the server
        etebase = Account.login(Client("python_test", SERVER_URL), username, password)
        col_mgr = etebase.get_collection_manager()
        cols = list(col_mgr.list(COL_TYPE, None).data)
        self.assertEqual(1, len(cols))
        self.assertEqual(b"Something else", bytes(cols[0].content))
        self.assertEqual("blap", cols[0].meta["bloop"])
        items = list(col_mgr.get_item_manager(cols[0]).list(None).data)
        self.assertEqual(1, len(items))
        self.assertEqual(b"Something item2", bytes(items[0].content))
        self.assertEqual({"type": "Bla", "bloop": "blap"}, items[0].meta)
        etebase.logout()
