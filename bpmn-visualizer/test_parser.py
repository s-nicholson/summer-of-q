"""
Tests for BPMN Parser
"""
import unittest
from bpmn_parser import BPMNParser, ElementType, ServiceTask, Task


class TestBPMNParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = BPMNParser()
    
    def test_parse_sample_file(self):
        """Test parsing the sample BPMN file"""
        processes = self.parser.parse_file('sample_process.bpmn')
        
        self.assertEqual(len(processes), 1)
        process = processes[0]
        
        self.assertEqual(process.id, 'sampleProcess')
        self.assertEqual(process.name, 'Sample Activiti Process')
        
        # Check we have the expected number of elements
        self.assertEqual(len(process.elements), 8)  # 1 start, 3 service tasks, 1 user task, 2 gateways, 1 end
        self.assertEqual(len(process.sequence_flows), 8)
    
    def test_service_task_parsing(self):
        """Test that service tasks are parsed with Activiti metadata"""
        processes = self.parser.parse_file('sample_process.bpmn')
        process = processes[0]
        
        # Find service task with class
        service_task = next(
            (elem for elem in process.elements 
             if elem.id == 'serviceTask1' and isinstance(elem, ServiceTask)), 
            None
        )
        
        self.assertIsNotNone(service_task)
        self.assertEqual(service_task.implementation_class, 'com.example.ProcessDataDelegate')
        self.assertEqual(service_task.name, 'Process Data')
        
        # Find service task with expression
        expr_task = next(
            (elem for elem in process.elements 
             if elem.id == 'serviceTask2' and isinstance(elem, ServiceTask)), 
            None
        )
        
        self.assertIsNotNone(expr_task)
        self.assertEqual(expr_task.expression, '${autoApprovalService.approve(execution)}')
    
    def test_user_task_parsing(self):
        """Test that user tasks are parsed with Activiti metadata"""
        processes = self.parser.parse_file('sample_process.bpmn')
        process = processes[0]
        
        user_task = next(
            (elem for elem in process.elements 
             if elem.id == 'userTask1' and isinstance(elem, Task)), 
            None
        )
        
        self.assertIsNotNone(user_task)
        self.assertEqual(user_task.assignee, 'reviewer')
        self.assertEqual(user_task.candidate_groups, 'managers,supervisors')
    
    def test_sequence_flow_conditions(self):
        """Test that sequence flow conditions are parsed"""
        processes = self.parser.parse_file('sample_process.bpmn')
        process = processes[0]
        
        # Find flow with condition
        conditional_flow = next(
            (flow for flow in process.sequence_flows 
             if flow.id == 'flow3'), 
            None
        )
        
        self.assertIsNotNone(conditional_flow)
        self.assertEqual(conditional_flow.condition_expression, '${needsReview == true}')
        self.assertEqual(conditional_flow.name, 'Needs Review')


if __name__ == '__main__':
    unittest.main()
