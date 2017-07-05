cwlVersion: v1.0
class: CommandLineTool
requirements:
  InlineJavascriptRequirement: {}
hints:
  DockerRequirement:
    dockerPull: kfang/svc_classify

stdout: $("svc_classified.txt")
baseCommand: ["python2"]

inputs:
  script:
    type: File
    inputBinding:
      position: 0 
  hiq_tiles:
    type: File
    inputBinding:
      position: 1
  names:
    type: File
    inputBinding:
      position: 2
  hiq_info:
    type: File
    inputBinding:
      position: 3
  assemblyGz:
    type: File
    inputBinding:
      position: 4
  assemblyFwi:
    type: File
    inputBinding:
      position: 5
    
outputs:
  svc_output:
    type: stdout
