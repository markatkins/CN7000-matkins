param (
    [string]$InputFile,
    [string]$OutputFile
)
#Join-Path -Path $PSScriptRoot -ChildPath "Templates\DocxTemplate.docx"
templatePath = "C:\Users\matkins\OneDrive - Cornelis Networks\Documents\Custom Office Templates\Standard_Tech Doc Word Template.docx"
#    --reference-doc=$templatePath `
#--toc=true --toc-depth=3 --lot=true --table-caption-position=above `
pandoc --from gfm --to docx --reference-doc=$templatePath --toc=true --toc-depth=3 --lot=true --table-caption-position=above -o $OutputFile $InputFile
    