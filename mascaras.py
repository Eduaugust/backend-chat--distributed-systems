def desmascarar_dados(mascara, dados):
    dados_desmascarados = bytearray()
    for i in range(len(dados)):
        dados_desmascarados.append(dados[i] ^ mascara[i % 4])
    return dados_desmascarados

def mascarar_dados(dados):
    payload_length = len(dados)
    frame_header = bytearray()

    frame_header.append(0x81)  # FIN e opcode (0x1 para texto)
    if payload_length <= 125:
        frame_header.append(payload_length)
    elif payload_length <= 65535:
        frame_header.append(126)
        frame_header.extend(payload_length.to_bytes(2, byteorder='big'))
    else:
        frame_header.append(127)
        frame_header.extend(payload_length.to_bytes(8, byteorder='big'))

    return frame_header + dados