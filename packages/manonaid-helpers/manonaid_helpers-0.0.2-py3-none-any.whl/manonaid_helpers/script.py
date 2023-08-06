from manonaid_helpers.download import Download

df = Download(
    destination="../test_data", source="cyi5", folder="pack_test/"
).returnAsDataFrameDict()
