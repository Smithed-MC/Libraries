from pytest_insta import SnapshotFixture

from beet import run_beet

def test_build(snapshot: SnapshotFixture):
    with run_beet(directory="smithed_libraries/packs/wiki") as ctx:
        assert snapshot("data_pack") == ctx.data
        assert snapshot("resource_pack") == ctx.assets