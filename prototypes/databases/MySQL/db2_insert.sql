USE `mydb`;
INSERT INTO FluxrepresentationTypes 
VALUES 
	('Fluxes'),
	('Matrices');	

INSERT INTO Models 
VALUES 
	("default_1.yaml","Hilbert"	,"Fluxes"  ),
	("default_2.yaml","Ceballos"	,"Fluxes"  ),
	("default_3.yaml","Ceballos_new","Matrices");

INSERT INTO Variables 
VALUES 
	( "x"  ,"default_1.yaml" ,"kg","root carbon stock"),
	( "y"  ,"default_1.yaml" ,"kg","leaf carbon stock"),
	( "k_r","default_1.yaml" ,"kg","root decomprate"  ),
	( "b_v1","default_1.yaml","kg","root decomprate"  );

INSERT INTO keytypes 
VALUES 
	('AllocationSplitVector','obvious');	

INSERT INTO keytypeSymbols
VALUES 
	('b','AllocationSplitVector');	

INSERT INTO Variables_has_keytypes 
VALUES 
	( "b_v1"  ,"default_1.yaml","AllocationSplitVector");
	
	
INSERT INTO StateVectorPositions 
VALUES 
        (1,"x","default_1.yaml"),
        (0,"y","default_1.yaml");

INSERT INTO InFluxes 
VALUES 
        ("x","default_1.yaml","x**1"),
        ("y","default_1.yaml","y**1");

INSERT INTO Outfluxes 
VALUES 
        ("x","default_1.yaml","x**3"),
        ("y","default_1.yaml","x**3");

INSERT INTO InternalFluxes 
VALUES 
        ("x","y","default_1.yaml","x**2"),
        ("y","x","default_1.yaml","y**2");

INSERT INTO CompartmentalMatricesAndInputVectors
VALUES 
        ("default_3.yaml","Matrix(x**3)","Vector(y)");

