{{indent}}if __condVld:
{{indent}}     yield (self.{{dst}}, mkUpdater({{src}}), {{isEventDependent}})
{{indent}}else:
{{indent}}     yield (self.{{dst}}, _invalidated(mkUpdater({{src}})), {{isEventDependent}})
