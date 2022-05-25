from brainflow.board_shim import BoardShim, BrainFlowInputParams
import logging, argparse, sys


sys.path.append('assets/temp')

class Device():
    def __init__(self,*args):
        f = open('assets/temp/serial','rb'); port = f.read().decode('utf-8'); f.close()
        
        BoardShim.enable_dev_board_logger()
        logging.basicConfig(level=logging.DEBUG)

        parser = argparse.ArgumentParser()
        # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
        parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                            default=10)
        parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
        parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                            default=0)
        parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
        parser.add_argument('--serial-port', type=str, help='serial port', required=False, default=port)
        parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
        parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
        parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
        parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
        parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                            required=False, default=0)
        parser.add_argument('--file', type=str, help='file', required=False, default='')
        args = parser.parse_args()

        params = BrainFlowInputParams()
        params.ip_port = args.ip_port
        params.serial_port = args.serial_port
        params.mac_address = args.mac_address
        params.other_info = args.other_info
        params.serial_number = args.serial_number
        params.ip_address = args.ip_address
        params.ip_protocol = args.ip_protocol
        params.timeout = args.timeout
        params.file = args.file

        try:
            self.board_shim = BoardShim(args.board_id, params)
            self.board_shim.prepare_session()
            self.board_shim.start_stream(450000, args.streamer_params)
        except BaseException:
            logging.warning('Exception', exc_info=True)

    def read(self,*args):
        return self.board_shim.get_current_board_data(1)[1:9]

    

    def close(self,*args):
        try:
            logging.info('End')
            if board_shim.is_prepared():
                logging.info('Releasing session')
                board_shim.release_session()
        except: pass
