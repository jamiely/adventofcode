import sys
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")

line = open('day16.input').readline().strip()

hex_to_bit={
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

def identity(x):
    return x

def less_than(ns):
    a, b = ns
    return 1 if a < b else 0

def greater_than(ns):
    a, b = ns
    return 1 if a > b else 0

def equal_to(ns):
    a, b = ns
    return 1 if a == b else 0

def product(ns):
    p = 1
    for n in ns:
        p *= n
    return p

operators = [
    {"type_id": 0, "name": "Σ", "func": sum},
    {"type_id": 1, "name": "∏", "func": product},
    {"type_id": 2, "name": "min", "func": min},
    {"type_id": 3, "name": "max", "func": max},
    {"type_id": 4, "name": "id", "func": identity},
    
    {"type_id": 5, "name": ">", "func": greater_than},
    {"type_id": 6, "name": "<", "func": less_than},
    {"type_id": 7, "name": "==", "func": equal_to},
]

operator_types = {}
for op in operators:
    operator_types[op["type_id"]] = op

def convert_hex(line):
    return ''.join([hex_to_bit[hex_char] for hex_char in list(line)])
bits = convert_hex(line)

bits_type_4 = "110100101111111000101000"
bits_type_other_0 = "00111000000000000110111101000101001010010001001000000000"
bits_type_other_1 = "11101110000000001101010000001100100000100011000001100000"

def process(bits, i):
    starting_bits = bits[i:]
    log.info("Processing bits starting at index=%d\n\t%s", i, starting_bits)
    memory = {"index": i, "packets": []}
    def consume(length):
        result = bits[memory["index"]:memory["index"]+length]
        memory["index"] += length
        return result

    def split_value():
        prefix = consume(1)
        rest = consume(4)
        return (prefix, rest)
        
    packet_version = consume(3)
    packet_type_id = consume(3)

    if packet_type_id == "100":
        value_pieces = []
        while True:
            (ap, av) = split_value()
            value_pieces.append(av)
            if ap != "1":
                break

        value = ''.join(value_pieces)
        decimal = int(value, 2)

        values = {
            "bits": starting_bits,
            "packet_version": packet_version,
            "packet_version_decimal": int(packet_version, 2),
            "packet_type_id": packet_type_id,
            "packet_type_id_decimal": int(packet_type_id, 2),
            "value_pieces": value_pieces,
            "value": value,
            "decimal_value": decimal,
            "packet_type": "literal",
        }

        memory["packets"].append(values)
    else:
        subpacket_count = None
        subpacket_count_decimal = None
        subpacket_length = None
        subpackets = None
        subpacket_length = None
        subpacket_length_decimal = None
        packets = []

        length_type_id = consume(1)
        if length_type_id == "0":
            subpacket_length = consume(15)
            subpacket_length_decimal = int(subpacket_length, 2)
            subpackets = consume(subpacket_length_decimal)

            logging.debug("Processing subpackets in bits length %d: %s", subpacket_length_decimal, subpackets)
            last_index = 0
            while True:
                last_memory = process(subpackets, last_index)
                if len(last_memory["packets"]) > 0:
                    packets.append(last_memory["packets"])
                if last_memory["index"] >= len(subpackets):
                    break
                last_index = last_memory["index"]
                log.debug("Continuing to extract subpackets\nlast_memory=\n%s", last_memory)
        else:
            subpacket_count = consume(11)
            subpacket_count_decimal = int(subpacket_count, 2)

            logging.debug("Processing %d subpackets", subpacket_count_decimal)
            for i in range(subpacket_count_decimal):
                last_memory = process(bits, memory["index"])
                memory["index"] = last_memory["index"]
                if len(last_memory["packets"]) > 0:
                    packets.append(last_memory["packets"])

        values = {
            "bits": starting_bits,
            "packet_version": packet_version,
            "packet_version_decimal": int(packet_version, 2),
            "packet_type_id": packet_type_id,
            "packet_type_id_decimal": int(packet_type_id, 2),
            
            "length_type": length_type_id,
            "subpacket_length": subpacket_length,
            "subpacket_length_decimal": subpacket_length_decimal,
            "subpackets": subpackets,
            "subpacket_count": subpacket_count,
            "subpacket_count_decimal": subpacket_count_decimal,
            "packet_type": "operator",
            "packets": packets
        }

        memory["packets"].append(values)

    # log.debug("values=%s", values)
    return memory


examples = [
    bits_type_4, 
    bits_type_other_0, 
    bits_type_other_1
]

# for bits in examples:
#     memory = process(bits, 0)
#     print(f"Got {len(memory['packets'])} packets.")

def log_packets(packet, memory, depth=1):
    log.debug("%spacket %d\n%s", '.' * (depth * 2), memory["count"], packet)

    if "packets" not in packet:
        return

    for p in packet["packets"]:
        memory["count"] += 1
        log_packets(p, memory, depth + 1)

def get_op(packet):
    try:
        return operator_types[packet["packet_type_id_decimal"]]
    except TypeError:
        log.error(packet)
        raise

def dump_packets(packets):
    memory = {"count": 0}

    def dp(packet, depth):
        if type(packet) == list:
            for p in packet:
                dp(p, depth + 1)
            return

        ptype = get_op(packet)["name"]
        if "value" in packet:
            log.debug("%s(%d) version=%s type=%s value=%s", '.' * (depth * 2), memory["count"], packet["packet_version_decimal"], ptype, packet["decimal_value"])
        else:
            log.debug("%s(%d) version=%s type=%s subpackets=%s", '.' * (depth * 2), memory["count"], packet["packet_version_decimal"], ptype, len(packet["packets"]))

        if "packets" not in packet:
            return

        for p in packet["packets"]:
            memory["count"] += 1
            dp(p, depth + 1)

    dp(packets, 0)

def version_sum(packets):
    mem = {"version_sum": 0}
    def vs(packets):
        if type(packets) == list:
            for p in packets:
                vs(p)
            return
        
        mem["version_sum"] += packets["packet_version_decimal"]

        if "packets" not in packets:
            return

        vs(packets["packets"])

    vs(packets)
    return mem["version_sum"]

def test(hex):
    log.info("Testing hex %s", hex)
    memory = process(convert_hex(hex), 0)
    log.info("packets: %d\nmemory:\n%s", len(memory["packets"]), memory)
    log_mem = {"count": 0}
    log.debug("@@@ Listing all packets")
    # for i in range(len(memory["packets"])):
    #     # log.debug("packet %d\n%s", i, memory["packets"][i])
    #     log_packets(memory["packets"][i], log_mem)

    dump_packets(memory["packets"])
    sum = version_sum(memory["packets"])
    log.info("memory sum %d", sum)
    result = run_operators(memory["packets"][0])
    log.info("operator result=%d", result)

def run_operators(packet):
    if type(packet) == list:
        results = [run_operators(p) for p in packet]
        if len(results) == 1:
            return results[0]
        return results
            
    op = get_op(packet)
    if op["name"] == "id":
        return packet["decimal_value"]
    
    try:
        operands = [run_operators(p) for p in packet["packets"]]
        return op["func"](operands)
    except TypeError:
        log.error("packet=%s\noperands=%s", packet, operands)
        raise

# test('8A004A801A8002F478')
# test('620080001611562C8802118E34')
# test('C0015000016115A2E0802F182340')
# test('A0016C880162017C3686B18A3D4780')
# test(line)
test(line)
