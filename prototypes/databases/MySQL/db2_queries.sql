USE `mydb`;
-- SELECT * FROM StateVectorPositions ;
-- get the statevector in correct order
SELECT Variables_symbol FROM StateVectorPositions WHERE Variables_model_id="default_1.yaml" ORDER BY `pos_id`;

-- get the fluxes of model 1
select expression from InFluxes where TargetVariables_model_id='default_1.yaml'; 

-- get the Matrices of model 1 (should be empty)
select CompartmentalMatrix,InputVector from CompartmentalMatricesAndInputVectors where model_id='default_1.yaml'; 

-- get the fluxes of model 3 (should be empty)
select expression from InFluxes where TargetVariables_model_id='default_3.yaml'; 

-- get the Matrices of model 3 
select CompartmentalMatrix,InputVector from CompartmentalMatricesAndInputVectors where model_id='default_3.yaml'; 

-- statevariables of model 1
select Variables_symbol From statevariables where Variables_model_id='default_1.yaml';

-- missing tests
-- make sure that for a model that has fluxrepresentation 'Fluxes' not matrices can be stored and also that 
-- for the models with fluxtype 'matrices' no fluxes can be stored 
-- Both things would be represented as a foreing key constraint to a view (which mysql does not implement) instead it has to be realized with triggered scripts
