CREATE DEFINER=`root`@`localhost` TRIGGER update_rea_score_in_assignment AFTER INSERT ON answer_score FOR EACH ROW 
update assignment as a inner join answer_score s on a.assign_id=s.assignment_id set a.rea_score=s.variable2 ;