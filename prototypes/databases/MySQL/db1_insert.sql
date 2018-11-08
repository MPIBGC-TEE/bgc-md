
USE `mydb`;
INSERT INTO Models 
VALUES 
	("default_1.yaml","Hilbert"),
	("default_2.yaml","Ceballos"),
	("default_3.yaml","Ceballos_new");

INSERT INTO Variables 
VALUES 
	("x","root carbon stock","kg","default_1.yaml"),
	( "y","leaf carbon stock","kg","default_1.yaml"),
	( "k_r","root decomprate","kg","default_1.yaml");
INSERT INTO StateVectorPositions 
VALUES 
        (0,"x","default_1.yaml"),
        (1,"y","default_1.yaml");
