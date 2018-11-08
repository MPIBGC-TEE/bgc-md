USE `mydb`;
INSERT INTO Models 
VALUES 
	("default_1.yaml","Hilbert"),
	("default_2.yaml","Ceballos"),
	("default_3.yaml","Ceballos_new");

INSERT INTO Variables 
VALUES 
	( "x"  ,"default_1.yaml","kg","root carbon stock"),
	( "y"  ,"default_1.yaml","kg","leaf carbon stock"),
	( "k_r","default_1.yaml","kg","root decomprate");

INSERT INTO StateVectorPositions 
VALUES 
        (1,"x","default_1.yaml"),
        (0,"y","default_1.yaml");
