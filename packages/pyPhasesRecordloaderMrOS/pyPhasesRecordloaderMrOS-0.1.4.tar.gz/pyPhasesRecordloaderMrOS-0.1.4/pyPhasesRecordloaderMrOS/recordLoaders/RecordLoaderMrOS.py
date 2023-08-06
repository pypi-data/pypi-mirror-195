from pyPhasesRecordloaderSHHS.recordLoaders.RecordLoaderSHHS import RecordLoaderSHHS

from pyPhasesRecordloader.downloader.Downloader import Downloader


class RecordLoaderMrOS(RecordLoaderSHHS):
    def getFilePathSignal(self, recordId):
        isVisit1 = recordId[:11] == "mros-visit1"
        dl = Downloader.get()
        pathEdfV1, _, pathEdfV2, _ = dl.basePathExtensionwise

        path = pathEdfV1 if isVisit1 else pathEdfV2

        return path + "/" + recordId + ".edf"

    def getFilePathAnnotation(self, recordId):
        isVisit1 = recordId[:11] == "mros-visit1"
        dl = Downloader.get()
        _, pathXmlV1, _, pathXmlV2 = dl.basePathExtensionwise

        path = pathXmlV1 if isVisit1 else pathXmlV2

        return path + "/" + recordId + "-nsrr.xml"

    def groupBy(self, name: str, recordIds):
        groupedRecords = {}
        if name == "patient":
            for recordId in recordIds:
                id = recordId[12:]

                if id not in groupedRecords:
                    groupedRecords[id] = []

                groupedRecords[id].append(recordId)
        return groupedRecords
