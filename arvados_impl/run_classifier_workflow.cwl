cwlVersion: v1.0
class: Workflow
requirements:
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: kfang/svc_classify

inputs:
  hiq_tiles:
    type: File
  names:
    type: File
  hiq_info:
    type: File
  assemblyGz:
    type: File
  assemblyFwi:
    type: File

outputs:
  svc_output:
    type: File
    outputSource: classify/svc_output

steps:
  classify:
   run: classifier.cwl
   in:
     hiq_tiles: hiq_tiles
     names: names
     hiq_info: hiq_info
     assemblyGz: assemblyGz
     assemblyFwi: assemblyFwi
   out: [svc_output]
