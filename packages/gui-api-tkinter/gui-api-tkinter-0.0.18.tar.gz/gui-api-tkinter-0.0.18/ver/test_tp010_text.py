import unittest

from pytest_ver import pth

from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger


# -------------------
class TestTp010(unittest.TestCase):
    page1 = None
    logger = None
    helper = None
    th = None

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

        services.th = GuiApiHarness()
        services.th.init()
        services.logger = Logger()
        services.helper = Helper()

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        services.helper.kill_process()
        self.assertFalse(services.helper.gui_process.is_alive())

        # uncomment for debugging
        # print(f'DBG {services.logger.lines}')

    # --------------------
    @classmethod
    def tearDownClass(cls):
        services.th.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp010(self):
        pth.proto.protocol('tp-010', 'check "set_text" function on Text Widget')
        pth.proto.add_objective('check that set_text() correctly sets text in an Text widget')
        pth.proto.add_objective('check that set_text() respond with accurate nak json objects')
        pth.proto.add_objective('check that set_text_on() correctly sets text in an Text widget')
        pth.proto.add_objective('check that set_text_on() respond with accurate nak json objects')
        pth.proto.add_objective('check that set_text_at() correctly sets text in an Text widget')
        pth.proto.add_objective('check that set_text_at() respond with accurate nak json objects')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{services.th.version}')

        pth.proto.step('start gui')
        # don't call callback
        services.helper.start_process()
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        services.th.connect()
        pth.ver.verify_true(services.th.is_connected())

        pth.proto.step('get page content')
        services.th.get_screen()
        pth.ver.verify_gt(len(services.th.content), 0)

        # uncomment for debug
        # import json
        # print(f'DBG {json.dumps(services.th.content, indent=4)}')

        pth.proto.step('check initial Text widget information')
        widget_path = ['window1', 'page1_frame', 'button_frame', 'text1']
        item = services.th.search(widget_path)
        pth.ver.verify_equal('Text', item['class'])
        pth.ver.verify_equal('text1', item['name'], reqids=['SRS-090'])
        pth.ver.verify_equal('\n', item['value'], reqids='SRS-090')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-090')

        # === set_text_on
        msg = 'text1abcd'
        pth.proto.step('enter a string into the Text widget')
        services.th.set_text_on(item, msg)
        services.th.get_screen()

        pth.proto.step('verify the contents of the Text widget have changed')
        item = services.th.search(widget_path)
        pth.ver.verify_equal('Text', item['class'])
        pth.ver.verify_equal('text1', item['name'])
        pth.ver.verify_equal(f'{msg}\n', item['value'], reqids=['SRS-092', 'SRS-091'])
        pth.ver.verify_equal('normal', item['state'])

        # === set_text()
        msg += 'e'
        pth.proto.step('set_text() on Text widget using search path')
        ack_nak = services.th.set_text(widget_path, msg)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the contents of the Text widget have changed to "abcde"')
        services.th.get_screen()
        item = services.th.search(widget_path)
        pth.ver.verify_equal(f'text1abcde\n', item['value'], reqids=['SRS-092', 'SRS-091'])

        # === set_text_at()
        msg += 'f\ng'
        pth.proto.step('set_text_at() on Text widget using raw x, y coordinates')
        button = services.th.search(widget_path)
        x = int((button['coordinates']['x1'] + button['coordinates']['x2']) / 2)
        y = int((button['coordinates']['y1'] + button['coordinates']['y2']) / 2)
        ack_nak = services.th.set_text_at(x, y, msg)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the contents of the Text widget have changed to "abcdef\\ng"')
        services.th.get_screen()
        item = services.th.search(widget_path)
        pth.ver.verify_equal('text1abcdef\ng\n', item['value'], reqids=['SRS-092', 'SRS-091'])

        # === clear text
        pth.proto.step('enter an empty string into the Text widget')
        ack_nak = services.th.set_text_at(x, y, '')
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the contents of the Text widget have changed to ""')
        services.th.get_screen()
        item = services.th.search(widget_path)
        pth.ver.verify_equal('\n', item['value'], reqids=['SRS-092', 'SRS-091'])

        # === set_text_on() invalid params
        pth.proto.step('set_text_on() with None item')
        ack_nak = services.th.set_text_on(None, 'g')
        pth.ver.verify_equal('set_text_on', ack_nak['rsp'], reqids=['SRS-094'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-094'])
        pth.ver.verify_equal('set text item is None', ack_nak['reason'], reqids=['SRS-094'])

        pth.proto.step('set_text_on() with missing coordinates')
        ack_nak = services.th.set_text_on({}, 'h')
        pth.ver.verify_equal('set_text_on', ack_nak['rsp'], reqids=['SRS-094'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-094'])
        pth.ver.verify_equal('set text item missing coordinates values', ack_nak['reason'], reqids=['SRS-094'])

        pth.proto.step('set_text_on() with None message')
        ack_nak = services.th.set_text_on(item, None)
        pth.ver.verify_equal('set_text_on', ack_nak['rsp'], reqids=['SRS-094'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-094'])
        pth.ver.verify_equal('set text msg is None', ack_nak['reason'], reqids=['SRS-094'])

        # Note: empty message is allowed

        # === set_text() invalid params
        pth.proto.step('set_text() with None path')
        ack_nak = services.th.set_text(None, 'i')
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('set text path is None', ack_nak['reason'], reqids=['SRS-093'])

        pth.proto.step('set_text() with empty path')
        ack_nak = services.th.set_text([], 'j')
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('set text path is empty', ack_nak['reason'], reqids=['SRS-093'])

        pth.proto.step('set_text() with unknown path')
        ack_nak = services.th.set_text(['windowx1'], 'k')
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('search path is not found', ack_nak['reason'], reqids=['SRS-093'])

        pth.proto.step('set_text() with None message')
        ack_nak = services.th.set_text(['window1'], None)
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('set text msg is None', ack_nak['reason'], reqids=['SRS-093'])

        # Note: empty message is allowed

        # === set_text_at() invalid params
        pth.proto.step('set_text_at() with bad x coordinate')
        ack_nak = services.th.set_text_at(1.23, 10, 'l')
        pth.ver.verify_equal('set_text_at', ack_nak['rsp'], reqids=['SRS-095'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-095'])
        pth.ver.verify_equal('set text x-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-095'])

        pth.proto.step('set_text_at() with bad y coordinate')
        ack_nak = services.th.set_text_at(10, 1.23, 'm')
        pth.ver.verify_equal('set_text_at', ack_nak['rsp'], reqids=['SRS-095'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-095'])
        pth.ver.verify_equal('set text y-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-095'])

        pth.proto.step('set_text_at() with None message')
        ack_nak = services.th.set_text_at(10, 20, None)
        pth.ver.verify_equal('set_text_at', ack_nak['rsp'], reqids=['SRS-095'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-095'])
        pth.ver.verify_equal('set text msg is None', ack_nak['reason'], reqids=['SRS-095'])

        # Note: empty message is allowed

        # === done, clear up
        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
