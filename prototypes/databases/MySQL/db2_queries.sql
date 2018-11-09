USE `mydb`;
-- SELECT * FROM StateVectorPositions ;
-- get the statevector in correct order
SELECT Variables_symbol FROM StateVectorPositions WHERE Variables_model_id="default_1.yaml" ORDER BY `pos_id`;

