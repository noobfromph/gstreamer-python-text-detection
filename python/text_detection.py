#!/usr/bin/python3

from utils.utils import gst_buffer_with_pad_to_ndarray
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import Gst, GObject, GstBase
import pytesseract

Gst.init(None)
FIXED_CAPS = Gst.Caps.from_string('video/x-raw,format=BGR,width=[1,2147483647],height=[1,2147483647]')

class TextDetectionPy(GstBase.BaseTransform):
 __gstmetadata__ = ('Text Detection Python', 'Transform', 'example element', 'homan')
 __gsttemplates__ = (
  Gst.PadTemplate.new("src", Gst.PadDirection.SRC, Gst.PadPresence.ALWAYS, FIXED_CAPS),
  Gst.PadTemplate.new("sink", Gst.PadDirection.SINK, Gst.PadPresence.ALWAYS, FIXED_CAPS)
 )
 _sinkpadtemplate = __gsttemplates__[1]
 __gproperties__ = {}
 
 caps = None
 run_detect = True

 def __init__(self): # bug workaround
  self._segmentation_fault_workaround_sink = Gst.Pad.new_from_template(Gst.PadTemplate.new("sink", Gst.PadDirection.SINK, Gst.PadPresence.ALWAYS, Gst.Caps.new_any()), "sink")
  self._segmentation_fault_workaround_sink.set_chain_function_full(self.chain)
 
 def do_set_caps(self, incaps, outcaps):
  self.caps = incaps
  return True
 
 def do_transform_ip(self, buf):
  A = gst_buffer_with_pad_to_ndarray(buf, self.caps)
  if self.run_detect:
   self.run_detect = False
   text_data = pytesseract.image_to_data(buf)
   print("Text detected: ", text_data)

  return Gst.FlowReturn.OK # always return

GObject.type_register(TextDetectionPy)
__gstelementfactory__ = ("text_detection_py", Gst.Rank.NONE, TextDetectionPy)
