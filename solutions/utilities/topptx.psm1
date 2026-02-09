param (
    [string]$InputFile,
    [string]$OutputFile
)
#Join-Path -Path $PSScriptRoot -ChildPath "Templates\DocxTemplate.docx"
templatePath = "C:\Users\matkins\OneDrive - Cornelis Networks\Documents\Custom Office Templates\Standard PPT Template_Dark.pptx"
templatePath = "custom-reference.pptx"
#    --reference-doc=$templatePath `
#--toc=true --toc-depth=3 --lot=true --table-caption-position=above `
print $templatePath
pandoc --from gfm --to pptx --reference-doc=$templatePath -o $OutputFile $InputFile
    