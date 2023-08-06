# from initializer import initialize
#
#
# class ScriptRunner:
#
#     def __init__(self):
#         pass
#
#     def start(self):
#
#
#         WasabiClient = initialize()
#
#         print(
#             f"{indicators.OKGREEN}Choose from the following list of operations to run on your Wasabi bucket: {WasabiClient.bucketName}"
#         )
#         print(
#             f"\t{indicators.OKMAGENTA}Operation 1: Delete Non-Current Objects {indicators.ENDC}"
#         )
#         print(
#             f"\t{indicators.OKMAGENTA}Operation 2: Delete Current and Non-Current Objects {indicators.ENDC}"
#         )
#         print(
#             f"\t{indicators.OKMAGENTA}Operation 3: Purge Delete Markers {indicators.ENDC}"
#         )
#         print(f"\t{indicators.OKMAGENTA}Operation 4: Delete Bucket {indicators.ENDC}")
#
#         acceptableOptions = [1, 2, 3, 4]
#         userSelection = int(
#             input(
#                 f"{indicators.WARNING}Select Operation (Number 1-4) : {indicators.ENDC}"
#             ).strip()
#         )
#
#         if userSelection not in acceptableOptions:
#             print(f"{indicators.FAIL}Wrong Option Selected :( Try again!{indicators.ENDC}")
#         else:
#             if userSelection == 1:
#                 WasabiClient.deleteNonCurrentsV2()
#             elif userSelection == 2:
#                 for i in range(4):
#                     WasabiClient.deleteVersionsandObjects()
#             elif userSelection == 3:
#                 WasabiClient.purgeDeleteMarkers()
#             elif userSelection == 4:
#                 WasabiClient.deleteBucket()
