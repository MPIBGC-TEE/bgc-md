This directory is constitutes the approved and continuously tested database. 
This has some major implications:
1.  All files in this directory are checked by the tests and have to pass. 
For file.yaml  that lives here we test that all reports implied by the contained data
can be created without error. 
If you know, for example, that a record has isufficient data to run the model remove this part in the yaml file.
If you work on myNewModel.yaml and do not pass all the tests yet do not put it here!

1. The file names in this folder have to be unique. In the database metaphor this directory represents a table the yaml files the records and the file name the unique key for a record.
If you several versions of a file describing the same model you can copy version you want here (or symlink if the file lives in the same  repository as this directory).

