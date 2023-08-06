"""Test for accessing change tables."""
import dask_deltasharing as dds

T = "test/test-profile.json#lynxkite-dev.default.silvertable"
v = dds.get_latest_table_version(T)
for version, action, df in dds.load_as_dask_changes(T, starting_version=4, ending_version=v):
    print(version, action)
    print(df.compute())
# Simply loading the whole table works too:
v = dds.load_as_dask(T)
