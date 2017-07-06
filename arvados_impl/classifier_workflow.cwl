cwlVersion: v1.0
class: Workflow
requirements:
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: kfang/svc_classify
  ResourceRequirement:
    ramMin: 16384
    ramMax: 32768

inputs:
  script:
    type: File
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
  pgp_survey:
    type: File

outputs:
  svc_output:
    type: File
    outputSource: classify/svc_output

steps:
  classify:
   run: classifier.cwl
   in:
     script: script
     hiq_tiles: hiq_tiles
     names: names
     hiq_info: hiq_info
     assemblyGz: assemblyGz
     assemblyFwi: assemblyFwi
     pgp_survey: pgp_survey
   out: [svc_output]
