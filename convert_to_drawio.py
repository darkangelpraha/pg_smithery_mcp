#!/usr/bin/env python3
"""
Convert Structurizr JSON to Draw.io XML format
Usage: python3 convert_to_drawio.py pg_icepanel_c4.json
"""

import json
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import html

def escape_xml(text):
    """Escape XML special characters"""
    if not text:
        return ""
    return html.escape(str(text))

def convert_structurizr_to_drawio(json_file_path, output_file_path=None):
    """Convert Structurizr JSON to Draw.io XML format"""
    
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create root mxfile element
    mxfile = ET.Element('mxfile')
    mxfile.set('host', 'app.diagrams.net')
    mxfile.set('modified', datetime.now().isoformat())
    mxfile.set('agent', 'Python Script')
    mxfile.set('version', '21.0.0')
    mxfile.set('type', 'device')
    
    # Create diagram element
    diagram = ET.SubElement(mxfile, 'diagram')
    diagram.set('id', str(data.get('id', '1')))
    diagram.set('name', data.get('name', 'Diagram'))
    
    # Create mxGraphModel
    mx_graph_model = ET.SubElement(diagram, 'mxGraphModel')
    mx_graph_model.set('dx', '1422')
    mx_graph_model.set('dy', '794')
    mx_graph_model.set('grid', '1')
    mx_graph_model.set('gridSize', '10')
    mx_graph_model.set('guides', '1')
    mx_graph_model.set('tooltips', '1')
    mx_graph_model.set('connect', '1')
    mx_graph_model.set('arrows', '1')
    mx_graph_model.set('fold', '1')
    mx_graph_model.set('page', '1')
    mx_graph_model.set('pageScale', '1')
    mx_graph_model.set('pageWidth', '2000')
    mx_graph_model.set('pageHeight', '2000')
    mx_graph_model.set('math', '0')
    mx_graph_model.set('shadow', '0')
    
    # Create root element
    root = ET.SubElement(mx_graph_model, 'root')
    
    # Root cells
    cell0 = ET.SubElement(root, 'mxCell')
    cell0.set('id', '0')
    
    cell1 = ET.SubElement(root, 'mxCell')
    cell1.set('id', '1')
    cell1.set('parent', '0')
    
    # Track element positions and IDs
    cell_id_counter = 2
    element_map = {}
    x_pos = 50
    y_pos = 50
    x_step = 250
    y_step = 150
    current_x = x_pos
    current_y = y_pos
    
    def get_next_cell_id():
        nonlocal cell_id_counter
        cell_id = str(cell_id_counter)
        cell_id_counter += 1
        return cell_id
    
    def create_cell(parent_id, value, style, x, y, width, height, vertex=True, edge=False, source=None, target=None):
        """Helper function to create a cell"""
        cell_id = get_next_cell_id()
        cell = ET.SubElement(root, 'mxCell')
        cell.set('id', cell_id)
        cell.set('parent', parent_id)
        if value:
            cell.set('value', escape_xml(value))
        if style:
            cell.set('style', style)
        if vertex:
            cell.set('vertex', '1')
        if edge:
            cell.set('edge', '1')
        if source:
            cell.set('source', source)
        if target:
            cell.set('target', target)
        
        geometry = ET.SubElement(cell, 'mxGeometry')
        if x is not None:
            geometry.set('x', str(x))
        if y is not None:
            geometry.set('y', str(y))
        if width:
            geometry.set('width', str(width))
        if height:
            geometry.set('height', str(height))
        if edge:
            geometry.set('relative', '1')
            geometry.set('as', 'geometry')
        
        return cell_id
    
    # Process People
    if 'people' in data.get('model', {}):
        for idx, person in enumerate(data['model']['people']):
            style = 'shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;'
            if person.get('location') == 'External':
                style += 'fillColor=#dae8fc;strokeColor=#6c8ebf;'
            else:
                style += 'fillColor=#d5e8d4;strokeColor=#82b366;'
            
            value = person.get('name', '')
            if person.get('description'):
                value += '\\n' + person.get('description', '')
            
            cell_id = create_cell(
                '1',
                value,
                style,
                current_x,
                current_y,
                120,
                80
            )
            element_map[person['id']] = cell_id
            
            current_x += x_step
            if (idx + 1) % 4 == 0:
                current_x = x_pos
                current_y += y_step
        
        current_y += y_step
        current_x = x_pos
    
    # Process Software Systems
    if 'softwareSystems' in data.get('model', {}):
        for idx, system in enumerate(data['model']['softwareSystems']):
            style = 'rounded=1;whiteSpace=wrap;html=1;'
            if system.get('location') == 'External':
                style += 'fillColor=#fff2cc;strokeColor=#d6b656;'
            else:
                style += 'fillColor=#d5e8d4;strokeColor=#82b366;'
            
            value = system.get('name', '')
            if system.get('description'):
                value += '\\n' + system.get('description', '')
            
            system_cell_id = create_cell(
                '1',
                value,
                style,
                current_x,
                current_y,
                200,
                100
            )
            element_map[system['id']] = system_cell_id
            
            # Process Containers
            if 'containers' in system:
                container_y = current_y + 120
                for c_idx, container in enumerate(system['containers']):
                    container_style = 'rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;'
                    container_value = container.get('name', '')
                    if container.get('description'):
                        container_value += '\\n' + container.get('description', '')
                    
                    container_cell_id = create_cell(
                        system_cell_id,
                        container_value,
                        container_style,
                        current_x + 20,
                        container_y,
                        160,
                        80
                    )
                    element_map[container['id']] = container_cell_id
                    
                    # Process Components
                    if 'components' in container:
                        component_y = container_y + 100
                        for comp_idx, component in enumerate(container['components']):
                            component_style = 'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;'
                            component_value = component.get('name', '')
                            if component.get('description'):
                                component_value += '\\n' + component.get('description', '')
                            
                            component_cell_id = create_cell(
                                container_cell_id,
                                component_value,
                                component_style,
                                current_x + 40,
                                component_y,
                                120,
                                60
                            )
                            element_map[component['id']] = component_cell_id
                            component_y += 80
                    
                    container_y += 100
            
            current_x += x_step * 2
            if (idx + 1) % 3 == 0:
                current_x = x_pos
                current_y += y_step * 2
    
    # Process Relationships
    if 'relationships' in data.get('model', {}):
        for rel in data['model']['relationships']:
            source_id = element_map.get(rel.get('sourceId'))
            target_id = element_map.get(rel.get('destinationId'))
            
            if source_id and target_id:
                rel_style = 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666666;'
                rel_value = rel.get('description', '')
                
                create_cell(
                    '1',
                    rel_value,
                    rel_style,
                    None,
                    None,
                    None,
                    None,
                    vertex=False,
                    edge=True,
                    source=source_id,
                    target=target_id
                )
    
    # Convert to string
    rough_string = ET.tostring(mxfile, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent='  ')
    
    # Remove extra blank lines
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    output = '\n'.join(lines)
    
    # Write output file
    if not output_file_path:
        output_file_path = json_file_path.replace('.json', '.drawio')
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✓ Converted {json_file_path} to {output_file_path}")
    return output_file_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 convert_to_drawio.py <input.json> [output.drawio]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        convert_structurizr_to_drawio(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
