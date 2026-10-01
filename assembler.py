instructions = {
    'NOP': '0000', 'HLT': '0001', 'ADD': '0010', 'SUB': '0011',
    'NOR': '0100', 'AND': '0101', 'XOR': '0110', 'RSH': '0111',
    'LDI': '1000', 'ADI': '1001', 'JMP': '1010', 'BRH': '1011',
    'CAL': '1100', 'RET': '1101', 'LOD': '1110', 'STR': '1111'
}
def assemble():
    with open('program.asm', 'r') as file:
        assembled_instruction = []
        for line in file:
            cleaned_line = line.strip()
            if not cleaned_line:
                continue
            if cleaned_line.startswith('#'):
                continue
            instruction = cleaned_line.split()
            pseudo_opcode = instruction[0]
            if pseudo_opcode == 'CMP':
                instruction = ['SUB', instruction[1], instruction[2], 'r0']
            elif pseudo_opcode == 'MOV':
                instruction = ['ADD', instruction[1], 'r0', instruction[2]]
            elif pseudo_opcode == 'LSH':
                instruction = ['ADD', instruction[1], instruction[1], instruction[2]]
            elif pseudo_opcode == 'INC':
                instruction = ['ADI', instruction[1], '1']
            elif pseudo_opcode == 'DEC':
                instruction = ['ADI', instruction[1], '-1']
            elif pseudo_opcode == 'NOT':
                instruction = ['NOR', instruction[1], 'r0', instruction[2]]
            elif pseudo_opcode == 'NEG':
                instruction = ['SUB', 'r0', instruction[1], instruction[2]]
            opcode = instruction[0]
            try:
                opcode_bin = instructions[opcode]
                if opcode in ['HLT', 'NOP', 'RET']:
                    assembled_instruction.append(opcode_bin + '000000000000')
                elif opcode in ['ADD', 'SUB', 'NOR', 'AND', 'XOR']:
                    operand = f'{int(instruction[1][1:]):04b}' + f'{int(instruction[2][1:]):04b}' + f'{int(instruction[3][1:]):04b}'
                    assembled_instruction.append(opcode_bin + operand)
                elif opcode == 'RSH':
                    operand = f'{int(instruction[1][1:]):04b}' + '0000' + f'{int(instruction[2][1:]):04b}' 
                    assembled_instruction.append(opcode_bin + operand)
                elif opcode in ['LDI', 'ADI']:
                    operand = f'{int(instruction[1][1:]):04b}' + f'{(int(instruction[2]) & 0xFF):08b}'
                    assembled_instruction.append(opcode_bin + operand)
                elif opcode in ['JMP', 'CAL', 'BRH']:
                    if opcode == 'BRH':
                        operand = instruction[1] + f'{int(instruction[2]):10b}'
                        assembled_instruction.append(opcode_bin + operand)
                    else:
                        operand = '00' + f'{int(instruction[2]):10b}'
                        assembled_instruction.append(opcode_bin + operand)
                elif opcode in ['LOD', 'STR']:
                    reg_a = int(instruction[1][1:]) if instruction[1].lower().startswith('r') else int(instruction[1])
                    reg_b = int(instruction[2][1:]) if instruction[2].lower().startswith('r') else int(instruction[2])
                    offset_val = 0
                    if len(instruction) > 3:
                        offset_val = int(instruction[3])
                    reg_a_bin = f'{reg_a:04b}'
                    reg_b_bin = f'{reg_b:04b}'
                    offset_bin = f'{(offset_val & 0xF):04b}'
                    operand = reg_a_bin + reg_b_bin + offset_bin
                    assembled_instruction.append(opcode_bin + operand)
            except Exception as e:
                print(f'an error occurred: {e}')
    return assembled_instruction
print(assemble())