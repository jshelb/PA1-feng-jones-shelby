#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  (based on code developed for Distributed Systems course in Fall 2019)
#  Modified: Fall 2022 (changed packet name to not confuse with pub/sub Messages)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using flatbuffers
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

# this is needed to tell python where to find the flatbuffers package
# make sure to change this path to where you have compiled and installed
# flatbuffers.  If the python package is installed in your system wide files
# or virtualenv, then this may not be needed
'''CHANGE PATH FOR URS'''
sys.path.append(os.path.join (os.path.dirname(__file__), '/home/jshelby/Apps/flatbuffers/python'))
import flatbuffers    # this is the flatbuffers package we import
import time   # we need this get current time
import numpy as np  # to use in our vector field

import zmq   # we need this for additional constraints provided by the zmq serialization

from custom_msg import CustomMessage  # our custom message in native format
from CustomAppProto import Health
from CustomAppProto import Order, VeggieOrder, CansAndBottles, Milk, Bread, Meat
from CustomAppProto import Response

import CustomAppProto.Health as health   # this is the generated code by the flatc compiler
import CustomAppProto.Order as order
import CustomAppProto.Response as response

# This is the method we will invoke from our driver program
# Note that if you have have multiple different message types, we could have
# separate such serialize/deserialize methods, or a single method can check what
# type of message it is and accordingly take actions.
def serialize (cm):
    ''' 
    TODO : 1. follow the format used to serialize the example msg and implement 
              for order, health, and response (shouldn't be hard)
           2. create a python representation of the schemas (see custom_msg.py -
               easy)
          - if u make changes to the fbs files, follow instructions in readme 
            to regenerate the py representation in the CustomAppProto dir
    '''
    # first obtain the builder object that is used to create an in-memory representation
    # of the serialized object from the custom message
    builder = flatbuffers.Builder (0);

    # create the name string for the name field using
    # the parameter we passed
    name_field = builder.CreateString (cm.name)
    
    # serialize our dummy array. The sample code in Flatbuffers
    # describes doing this in reverse order
    msg.StartDataVector (builder, len (cm.vec))
    for i in reversed (range (len (cm.vec))):
        builder.PrependUint32 (cm.vec[i])
    data = builder.EndVector ()
    
    # let us create the serialized msg by adding contents to it.
    # Our custom msg consists of a seq num, timestamp, name, and an array of uint32s
    msg.Start (builder)  # serialization starts with the "Start" method
    msg.AddSeqNo (builder, cm.seq_num)
    msg.AddTs (builder, cm.ts)   # serialize current timestamp
    msg.AddName (builder, name_field)  # serialize the name
    msg.AddData (builder, data)  # serialize the dummy data
    serialized_msg = msg.End (builder)  # get the topic of all these fields


    # Serialize the data array
    Health.HealthStartDataVector(builder, len(cm.data))
    for i in reversed(range(len(cm.data))):
        builder.PrependUint32(cm.data[i])
    data = builder.EndVector()

    # Serialize the Health message
    Health.HealthStart(builder)
    Health.HealthAddSeqNo(builder, cm.seq_no)
    Health.HealthAddTs(builder, cm.ts)
    Health.HealthAddName(builder, name_field)
    Health.HealthAddData(builder, data)
    Health.HealthAddDispenser(builder, cm.dispenser)
    Health.HealthAddIcemaker(builder, cm.icemaker)
    Health.HealthAddLightbulb(builder, cm.lightbulb)
    Health.HealthAddFridgeTemp(builder, cm.fridge_temp)
    Health.HealthAddFreezerTemp(builder, cm.freezer_temp)
    Health.HealthAddSensorStatus(builder, cm.sensor_status)
    Health.HealthAddHumidity(builder, cm.humidity)
    Health.HealthAddDoorOpenings(builder, cm.door_openings)
    serialized_msg = Health.HealthEnd(builder)


    # Serialize the data array
    Order.OrderStartDataVector(builder, len(order.data))
    for i in reversed(range(len(order.data))):
        builder.PrependUint32(order.data[i])
    data = builder.EndVector()

    # Serialize the VeggieOrder table
    veggies = VeggieOrder.VeggieOrderCreate(
        builder,
        order.veggies.tomato,
        order.veggies.cucumber,
        order.veggies.eggplant,
        order.veggies.broccoli,
        order.veggies.carrot,
        order.veggies.onion
    )

    # Serialize the CansAndBottles table
    cans_and_bottles = CansAndBottles.CansAndBottlesCreate(
        builder,
        order.drinks.cans.coke,
        order.drinks.cans.pepsi,
        order.drinks.cans.coors,
        order.drinks.bottles.sprite,
        order.drinks.bottles.rootbeer,
        order.drinks.bottles.fanta
    )

    # Serialize the Milk vector
    milk_vector = []
    for milk_item in order.milk:
        milk_vector.append(Milk.MilkCreate(builder, milk_item.type, milk_item.quantity))
    Order.OrderStartMilkVector(builder, len(milk_vector))
    for milk_item in reversed(milk_vector):
        builder.PrependUOffsetTRelative(milk_item)
    milk = builder.EndVector(len(milk_vector))

    # Serialize the Bread vector
    bread_vector = []
    for bread_item in order.bread:
        bread_vector.append(Bread.BreadCreate(builder, bread_item.type, bread_item.quantity))
    Order.OrderStartBreadVector(builder, len(bread_vector))
    for bread_item in reversed(bread_vector):
        builder.PrependUOffsetTRelative(bread_item)
    bread = builder.EndVector(len(bread_vector))

    # Serialize the Meat vector
    meat_vector = []
    for meat_item in order.meat:
        meat_vector.append(Meat.MeatCreate(builder, meat_item.type, meat_item.quantity))
    Order.OrderStartMeatVector(builder, len(meat_vector))
    for meat_item in reversed(meat_vector):
        builder.PrependUOffsetTRelative(meat_item)
    meat = builder.EndVector(len(meat_vector))

    # Serialize the Order message
    Order.OrderStart(builder)
    Order.OrderAddSeqNo(builder, order.seq_no)
    Order.OrderAddTs(builder, order.ts)
    Order.OrderAddName(builder, name_field)
    Order.OrderAddData(builder, data)
    Order.OrderAddVeggies(builder, veggies)
    Order.OrderAddDrinks(builder, cans_and_bottles)
    Order.OrderAddMilk(builder, milk)
    Order.OrderAddBread(builder, bread)
    Order.OrderAddMeat(builder, meat)
    serialized_msg = Order.OrderEnd(builder)


    # Serialize the data array
    Response.ResponseStartDataVector(builder, len(response.data))
    for i in reversed(range(len(response.data))):
        builder.PrependUint32(response.data[i])
    data = builder.EndVector()

    # Serialize the Response message
    Response.ResponseStart(builder)
    Response.ResponseAddSeqNo(builder, response.seq_no)
    Response.ResponseAddTs(builder, response.ts)
    Response.ResponseAddName(builder, name_field)
    Response.ResponseAddData(builder, data)
    Response.ResponseAddCode(builder, response.code)
    Response.ResponseAddContents(builder, response.contents)
    serialized_msg = Response.ResponseEnd(builder)



    # end the serialization process
    builder.Finish (serialized_msg)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  # We had to do it this way because the send_serialized method of zmq under the hood
  # relies on send_multipart, which needs a list or sequence of frames. The easiest way
  # to get an iterable out of the serialized buffer is to enclose it inside []
  print ("serialize custom message to iterable list")
  return [serialize (cm)]
  
  
# deserialize the incoming serialized structure into native data type
def deserialize (buf):
    cm = CustomMessage ()
    
    packet = msg.Message.GetRootAs (buf, 0)

    # sequence number
    cm.seq_num = packet.SeqNo ()

    # timestamp received
    cm.ts = packet.Ts ()

    # name received
    cm.name = packet.Name ()

    # received vector data
    # We can obtain the vector like this but it changes the
    # type from List to NumpyArray, which may not be what one wants.
    #cm.vec = packet.DataAsNumpy ()
    cm.vec = [packet.Data (j) for j in range (packet.DataLength ())]

    return cm
    
# deserialize from frames
def deserialize_from_frames (recvd_seq):
  """ This is invoked on list of frames by zmq """

  # For this sample code, since we send only one frame, hopefully what
  # comes out is also a single frame. If not some additional complexity will
  # need to be added.
  assert (len (recvd_seq) == 1)
  #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
  print ("received data over the wire = {}".format (recvd_seq[0]))
  cm = deserialize (recvd_seq[0])  # hand it to our deserialize method

  # assuming only one frame in the received sequence, we just send this deserialized
  # custom message
  return cm
    
