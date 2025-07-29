"""
BPMN 2.0 XML Parser with Activiti support
"""
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class ElementType(Enum):
    START_EVENT = "startEvent"
    END_EVENT = "endEvent"
    SERVICE_TASK = "serviceTask"
    USER_TASK = "userTask"
    EXCLUSIVE_GATEWAY = "exclusiveGateway"
    PARALLEL_GATEWAY = "parallelGateway"
    SEQUENCE_FLOW = "sequenceFlow"
    PROCESS = "process"


@dataclass
class BPMNElement:
    """Base class for BPMN elements"""
    id: str
    name: Optional[str]
    element_type: ElementType
    activiti_metadata: Dict[str, Any]


@dataclass
class SequenceFlow(BPMNElement):
    """Represents a sequence flow between elements"""
    source_ref: str
    target_ref: str
    condition_expression: Optional[str] = None


@dataclass
class Task(BPMNElement):
    """Base class for tasks"""
    assignee: Optional[str] = None
    candidate_groups: Optional[str] = None
    candidate_users: Optional[str] = None


@dataclass
class ServiceTask(Task):
    """Service task with class implementation"""
    implementation_class: Optional[str] = None
    expression: Optional[str] = None


@dataclass
class Process:
    """BPMN Process container"""
    id: str
    name: Optional[str]
    elements: List[BPMNElement]
    sequence_flows: List[SequenceFlow]


class BPMNParser:
    """Parser for BPMN 2.0 XML files with Activiti support"""
    
    BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
    ACTIVITI_NS = "http://activiti.org/bpmn"
    
    def __init__(self):
        self.namespaces = {
            'bpmn': self.BPMN_NS,
            'activiti': self.ACTIVITI_NS
        }
    
    def parse_file(self, file_path: str) -> List[Process]:
        """Parse BPMN file and return list of processes"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        processes = []
        for process_elem in root.findall('.//bpmn:process', self.namespaces):
            process = self._parse_process(process_elem)
            processes.append(process)
        
        return processes
    
    def _parse_process(self, process_elem) -> Process:
        """Parse a single process element"""
        process_id = process_elem.get('id')
        process_name = process_elem.get('name')
        
        elements = []
        sequence_flows = []
        
        # Parse all child elements
        for child in process_elem:
            element = self._parse_element(child)
            if element:
                if isinstance(element, SequenceFlow):
                    sequence_flows.append(element)
                else:
                    elements.append(element)
        
        return Process(
            id=process_id,
            name=process_name,
            elements=elements,
            sequence_flows=sequence_flows
        )
    
    def _parse_element(self, elem) -> Optional[BPMNElement]:
        """Parse individual BPMN element"""
        tag = elem.tag.split('}')[-1]  # Remove namespace
        element_id = elem.get('id')
        name = elem.get('name')
        
        # Extract Activiti metadata
        activiti_metadata = self._extract_activiti_metadata(elem)
        
        if tag == 'startEvent':
            return BPMNElement(element_id, name, ElementType.START_EVENT, activiti_metadata)
        
        elif tag == 'endEvent':
            return BPMNElement(element_id, name, ElementType.END_EVENT, activiti_metadata)
        
        elif tag == 'serviceTask':
            return ServiceTask(
                id=element_id,
                name=name,
                element_type=ElementType.SERVICE_TASK,
                activiti_metadata=activiti_metadata,
                implementation_class=elem.get(f'{{{self.ACTIVITI_NS}}}class'),
                expression=elem.get(f'{{{self.ACTIVITI_NS}}}expression')
            )
        
        elif tag == 'userTask':
            return Task(
                id=element_id,
                name=name,
                element_type=ElementType.USER_TASK,
                activiti_metadata=activiti_metadata,
                assignee=elem.get(f'{{{self.ACTIVITI_NS}}}assignee'),
                candidate_groups=elem.get(f'{{{self.ACTIVITI_NS}}}candidateGroups'),
                candidate_users=elem.get(f'{{{self.ACTIVITI_NS}}}candidateUsers')
            )
        
        elif tag == 'exclusiveGateway':
            return BPMNElement(element_id, name, ElementType.EXCLUSIVE_GATEWAY, activiti_metadata)
        
        elif tag == 'parallelGateway':
            return BPMNElement(element_id, name, ElementType.PARALLEL_GATEWAY, activiti_metadata)
        
        elif tag == 'sequenceFlow':
            condition_expr = None
            condition_elem = elem.find('.//bpmn:conditionExpression', self.namespaces)
            if condition_elem is not None:
                condition_expr = condition_elem.text
            
            return SequenceFlow(
                id=element_id,
                name=name,
                element_type=ElementType.SEQUENCE_FLOW,
                activiti_metadata=activiti_metadata,
                source_ref=elem.get('sourceRef'),
                target_ref=elem.get('targetRef'),
                condition_expression=condition_expr
            )
        
        return None
    
    def _extract_activiti_metadata(self, elem) -> Dict[str, Any]:
        """Extract all Activiti-specific attributes and child elements"""
        metadata = {}
        
        # Extract Activiti attributes
        for attr_name, attr_value in elem.attrib.items():
            if attr_name.startswith(f'{{{self.ACTIVITI_NS}}}'):
                clean_name = attr_name.split('}')[-1]
                metadata[f'activiti:{clean_name}'] = attr_value
        
        # Extract Activiti child elements (like form properties)
        for child in elem:
            if child.tag.startswith(f'{{{self.ACTIVITI_NS}}}'):
                tag_name = child.tag.split('}')[-1]
                if tag_name == 'formProperty':
                    if 'form_properties' not in metadata:
                        metadata['form_properties'] = []
                    metadata['form_properties'].append({
                        'id': child.get('id'),
                        'name': child.get('name'),
                        'type': child.get('type'),
                        'required': child.get('required') == 'true'
                    })
        
        return metadata
