"""
BPMN Diagram Visualizer using Graphviz
"""
import graphviz
from typing import List, Dict, Optional
from bpmn_parser import Process, BPMNElement, SequenceFlow, ServiceTask, Task, ElementType


class BPMNVisualizer:
    """Creates visual diagrams from parsed BPMN processes"""
    
    def __init__(self, show_metadata: bool = False):
        self.show_metadata = show_metadata
        self.element_shapes = {
            ElementType.START_EVENT: 'circle',
            ElementType.END_EVENT: 'doublecircle',
            ElementType.SERVICE_TASK: 'box',
            ElementType.USER_TASK: 'box',
            ElementType.EXCLUSIVE_GATEWAY: 'diamond',
            ElementType.PARALLEL_GATEWAY: 'diamond'
        }
        self.element_colors = {
            ElementType.START_EVENT: 'lightgreen',
            ElementType.END_EVENT: 'lightcoral',
            ElementType.SERVICE_TASK: 'lightblue',
            ElementType.USER_TASK: 'lightyellow',
            ElementType.EXCLUSIVE_GATEWAY: 'orange',
            ElementType.PARALLEL_GATEWAY: 'purple'
        }
    
    def create_diagram(self, processes: List[Process], output_format: str = 'png') -> graphviz.Digraph:
        """Create a Graphviz diagram from BPMN processes"""
        dot = graphviz.Digraph(comment='BPMN Process Diagram')
        dot.attr(rankdir='LR', size='12,8')
        dot.attr('node', fontname='Arial', fontsize='10')
        dot.attr('edge', fontname='Arial', fontsize='8')
        
        for process in processes:
            self._add_process_to_diagram(dot, process)
        
        return dot
    
    def _add_process_to_diagram(self, dot: graphviz.Digraph, process: Process):
        """Add a single process to the diagram"""
        # Create subgraph for process
        with dot.subgraph(name=f'cluster_{process.id}') as process_graph:
            process_graph.attr(label=f'Process: {process.name or process.id}')
            process_graph.attr(style='rounded,filled', fillcolor='lightgray')
            
            # Add elements
            for element in process.elements:
                self._add_element_to_diagram(process_graph, element)
            
            # Add sequence flows
            for flow in process.sequence_flows:
                self._add_sequence_flow_to_diagram(dot, flow)
    
    def _add_element_to_diagram(self, graph: graphviz.Digraph, element: BPMNElement):
        """Add a BPMN element to the diagram"""
        shape = self.element_shapes.get(element.element_type, 'box')
        color = self.element_colors.get(element.element_type, 'white')
        
        # Build label
        label = self._build_element_label(element)
        
        graph.node(
            element.id,
            label=label,
            shape=shape,
            style='filled',
            fillcolor=color
        )
    
    def _build_element_label(self, element: BPMNElement) -> str:
        """Build label for element including metadata if requested"""
        label_parts = []
        
        # Element name
        if element.name:
            label_parts.append(element.name)
        else:
            label_parts.append(element.id)
        
        if self.show_metadata:
            # Add type-specific metadata
            if isinstance(element, ServiceTask):
                if element.implementation_class:
                    label_parts.append(f"Class: {element.implementation_class}")
                if element.expression:
                    label_parts.append(f"Expr: {element.expression}")
            
            elif isinstance(element, Task):
                if element.assignee:
                    label_parts.append(f"Assignee: {element.assignee}")
                if element.candidate_groups:
                    label_parts.append(f"Groups: {element.candidate_groups}")
                if element.candidate_users:
                    label_parts.append(f"Users: {element.candidate_users}")
            
            # Add general Activiti metadata
            for key, value in element.activiti_metadata.items():
                if key.startswith('activiti:') and value:
                    clean_key = key.replace('activiti:', '')
                    label_parts.append(f"{clean_key}: {value}")
        
        return '\\n'.join(label_parts)
    
    def _add_sequence_flow_to_diagram(self, graph: graphviz.Digraph, flow: SequenceFlow):
        """Add sequence flow to diagram"""
        label = ""
        if flow.name:
            label = flow.name
        
        if self.show_metadata and flow.condition_expression:
            if label:
                label += f"\\n[{flow.condition_expression}]"
            else:
                label = f"[{flow.condition_expression}]"
        
        graph.edge(
            flow.source_ref,
            flow.target_ref,
            label=label
        )
    
    def save_diagram(self, diagram: graphviz.Digraph, output_path: str, format: str = 'png'):
        """Save diagram to file"""
        diagram.format = format
        diagram.render(output_path, cleanup=True)
        print(f"Diagram saved to {output_path}.{format}")


def main():
    """Main function for command line usage"""
    import argparse
    from bpmn_parser import BPMNParser
    
    parser = argparse.ArgumentParser(description='Visualize BPMN 2.0 diagrams')
    parser.add_argument('input_file', help='Input BPMN XML file')
    parser.add_argument('--output', '-o', default='bpmn_diagram', 
                       help='Output file name (without extension)')
    parser.add_argument('--format', '-f', default='png', 
                       choices=['png', 'svg', 'pdf'],
                       help='Output format')
    parser.add_argument('--show-metadata', action='store_true',
                       help='Show Activiti metadata in diagram')
    
    args = parser.parse_args()
    
    try:
        # Parse BPMN file
        parser = BPMNParser()
        processes = parser.parse_file(args.input_file)
        
        if not processes:
            print("No processes found in BPMN file")
            return
        
        # Create visualization
        visualizer = BPMNVisualizer(show_metadata=args.show_metadata)
        diagram = visualizer.create_diagram(processes, args.format)
        
        # Save diagram
        visualizer.save_diagram(diagram, args.output, args.format)
        
        # Print summary
        total_elements = sum(len(p.elements) for p in processes)
        total_flows = sum(len(p.sequence_flows) for p in processes)
        print(f"Processed {len(processes)} process(es)")
        print(f"Total elements: {total_elements}")
        print(f"Total sequence flows: {total_flows}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
