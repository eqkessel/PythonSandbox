# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 20:53:51 2019

@author: redne
"""

import logging # Logging and debug printing
import atexit  # For running code at exit
from enum import Enum, auto # Enumerated types for reference

intcodeLog = logging.getLogger('intcode.log')
intcodeLog.setLevel(logging.DEBUG)
logFormat = logging.Formatter('\033[30;47m{name}[{levelname:*^8}]\033[39;49m: \033[3m{message}\033[0m', style='{')

# Running Modes enum
class RunModes(Enum):
    UNTIL_EXIT      = auto()
    UNTIL_OUTPUT    = auto()

class Interpreter:
    machines_defined = 0
    
    # CONSTRUCTOR
    def __init__(self, aPrgmInput, *, aName = 'Interpreter', aLevel = logging.WARNING,
                 aRunMode = RunModes.UNTIL_EXIT):
        self.machineID_ = Interpreter.machines_defined
        Interpreter.machines_defined += 1
        
        # Set up logging
        self.log_ = logging.getLogger('intcode.log.{name}{idnm:0>2}'.format(name = aName, idnm = self.machineID_))
        self.log_.setLevel(aLevel)
        
        self.logStream_ = logging.NullHandler()
        self.logStream_.setLevel(aLevel)
        
        if (self.log_.hasHandlers()):
            self.log_.removeHandler(self.logStream_)
        self.log_.addHandler(self.logStream_)
        
        self.log_.info("Initializing Intcode interpreter...")
        
        # This dictionary stores operation functions
        self.OPERATIONS = { 
            '01': {'func':self.__add, 'nparams':3},    # Sum operation
            '02': {'func':self.__mul, 'nparams':3},    # Multiply
            '03': {'func':self.__inp, 'nparams':1},    # Take input
            '04': {'func':self.__out, 'nparams':1},    # Produce output
            '05': {'func':self.__jtr, 'nparams':2},    # Jump if true
            '06': {'func':self.__jfs, 'nparams':2},    # Jump if false
            '07': {'func':self.__les, 'nparams':3},    # Less than comparison
            '08': {'func':self.__eqa, 'nparams':3},    # Equal comparison
            '99': {'func':self.__end, 'nparams':0},    # Terminate program
            'EE': {'func':self.__err, 'nparams':0}}    # Error-handling subroutine
        
        # This dictionary stores lambda functions to dereference what parameters
        # mean based on OpCode modes
        self.DEREF_PARAM = {
            0: lambda p: self.mem_[p],
            1: lambda p: p}
        
        self.runMode_ = aRunMode
        
        self.running_ = False
        self.program(aPrgmInput)

    # DESTRUCTOR
    @atexit.register
    def __del__(self):
        self.log_.info("Deleting Intcode interpreter")
        self.log_.removeHandler(self.logStream_)
        del self.logStream_, self.log_

    # TODO - Add logging and debug functionality
    # Add operation
    def __add(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        in1 = self.DEREF_PARAM[aOpr['getMode'](0)](aOpr['params'][0])
        in2 = self.DEREF_PARAM[aOpr['getMode'](1)](aOpr['params'][1])
        output = in1 + in2
        self.log_.debug("Summed {0} + {1} = {2}".format(in1,in2,output))
        self.mem_[aOpr['params'][-1]] = output
        return nextIp
    
    # Multiply operation
    def __mul(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        in1 = self.DEREF_PARAM[aOpr['getMode'](0)](aOpr['params'][0])
        in2 = self.DEREF_PARAM[aOpr['getMode'](1)](aOpr['params'][1])
        output = in1 * in2
        self.log_.debug("Multiplied {0} x {1} = {2}".format(in1,in2,output))
        self.mem_[aOpr['params'][-1]] = output
        return nextIp
    
    # Input operation
    def __inp(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        try:
            in1 = self.inBuffer_.pop(0)
        except IndexError:
            in1 = input("Program requesting input but buffer is empty!\nPlease provide an input:")
        self.log_.debug("Loaded {0}".format(in1))
        self.mem_[aOpr['params'][-1]] = in1
        return nextIp
    
    # Output operation
    def __out(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        in1 = self.DEREF_PARAM[aOpr['getMode'](0)](aOpr['params'][0])
        self.outBuffer_.append(in1)
        self.log_.debug("Outputed {0}".format(in1))
        self.dataReady_ = True
        return nextIp
    
    # Jump-if-true operation
    def __jtr(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        in1 = self.DEREF_PARAM[aOpr['getMode'](0)](aOpr['params'][0])
        in2 = self.DEREF_PARAM[aOpr['getMode'](1)](aOpr['params'][1])
        if (in1 != 0):  # Non-zero --> jump
            nextIp = in2
            self.log_.debug("Jumped to {1}: {0} 'True'".format(in1,in2))
        else:           # Pass
            self.log_.debug("Passing: {0} 'False'".format(in1))
            pass
        return nextIp
    
    # Jump-if-false operation
    def __jfs(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        in1 = self.DEREF_PARAM[aOpr['getMode'](0)](aOpr['params'][0])
        in2 = self.DEREF_PARAM[aOpr['getMode'](1)](aOpr['params'][1])
        if (in1 == 0):  # Zero --> jump
            nextIp = in2
            self.log_.debug("Jumped to {1}: {0} 'False'".format(in1,in2))
        else:           # Pass
            self.log_.debug("Passing: {0} 'True'".format(in1))
            pass
        return nextIp
    
    # Less-than conditional operation
    def __les(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        in1 = self.DEREF_PARAM[aOpr['getMode'](0)](aOpr['params'][0])
        in2 = self.DEREF_PARAM[aOpr['getMode'](1)](aOpr['params'][1])
        if (in1 < in2):
            self.log_.debug("{0} <{1}: Setting True".format(in1,in2))
            output = 1
        else:
            self.log_.debug("{0}!<{1}: Setting False".format(in1,in2))
            output = 0
        self.mem_[aOpr['params'][-1]] = output
        return nextIp
    
    # Equal-to conditional operation
    def __eqa(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        in1 = self.DEREF_PARAM[aOpr['getMode'](0)](aOpr['params'][0])
        in2 = self.DEREF_PARAM[aOpr['getMode'](1)](aOpr['params'][1])
        if (in1 == in2):
            self.log_.debug("{0}=={1}: Setting True".format(in1,in2))
            output = 1
        else:
            self.log_.debug("{0}!={1}: Setting False".format(in1,in2))
            output = 0
        self.mem_[aOpr['params'][-1]] = output
        return nextIp
    
    # Program exit operation
    def __end(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        self.log_.info("End expression encountered, exiting...")
        self.running_ = False
        return nextIp
    
    # Unknown operation
    def __err(self, aOpr):
        nextIp = aOpr['adr'] + aOpr['opDict']['nparams'] + 1
        self.running_ = False
        self.log_.critical("Unknown command encountered at address %d", aOpr['adr'])
        # TODO - add more error handling
        return nextIp
    
    # Pack operation into a dictionary; creates data + functionality
    def __getOper(self, aAddress):
        # This code is based off the fact that dictionaries returned from functions
        # can use lambda functions that reference themselves to add functionality
        # like a class that isn't encapsulated like an internal class (which can't
        # see its outer class in Python).
        # This is the most Wile E. Coyote level of programming I've ever done but
        # it just may work!
        opr = {'adr':aAddress}
        opr['raw'] = self.mem_[aAddress]
        codeStr = str(opr['raw'])
        opr['code'] = '{:0>2}'.format(codeStr[-2:])
        opr['modes'] = [int(i) for i in codeStr[-3::-1]]
        
        # If OpCode invalid pick error handling subroutine
        opr['opDict'] = self.OPERATIONS.get(opr['code'], self.OPERATIONS['EE'])
        slicer = slice(int(opr['adr']) + 1, int(opr['adr']+opr['opDict']['nparams']) + 1)
        opr['params'] = self.mem_[slicer]
        
        # The magic lines
        opr['run'] = lambda: self.__runOper(opr)
        opr['getMode'] = lambda n: opr['modes'][n] if (n < len(opr['modes'])) else 0
        #opr['print'] = lambda: self.printOpr(opr) # UNUSED
        
        # TODO - Set up different debug levels to help reduce spam on debug?
        #self.log_.debug("Operation is {}".format(opr))
        return opr
    
    # Function to run an operation. Alternatively operation['opDict']['func']() should work
    def __runOper(self, aOpr):
        self.callStack_.append(aOpr)
        func = aOpr['opDict']['func']
        return func(aOpr)
    
    # Check to see if machine needs to halt
    def __shouldContinue(self):
        output = True
        if (not self.running_):
            output = False
        if (self.runMode_ == RunModes.UNTIL_OUTPUT and self.dataReady_):
            self.dataReady_ = False
            output = False
        # TODO - Add manual clocking functionality with buttion presses for debugging
        return output        
    
    # (Re)program machine
    def program(self, aPrgmInput):
        if (self.running_):
            self.log_.warning("Cannot reprogram Intcode machine while running!")
            return
        self.log_.info("Programing...")
        
        self.prgmRaw_ = aPrgmInput
        self.prgm_ = [int (n) for n in self.prgmRaw_.split(",")]
        self.reboot()
    
    # Reset machine memory and instruction pointer    
    def reboot(self):
        self.log_.info("Rebooting...")
        
        self.running_ = False
        self.mem_ = self.prgm_.copy()
        #print(self.mem_)
        self.ip_ = 0            # Instruction pointer
        self.opCount_ = 0       # Operation counter
        self.inBuffer_ = []     # Input buffer
        self.outBuffer_ = []    # Output buffer
        self.dataReady_ = False # Buffer has new data
        self.callStack_ = []    # Debugging aid
    
    # Run single instruction    
    def clock(self):
        currOper = self.__getOper(self.ip_)
        self.ip_ = currOper['run']()
    
    # Automatically clock until halting
    def run(self):
        self.running_ = True
        self.log_.info("Running program...")
        while(self.__shouldContinue()):
            self.log_.debug("IP:{0:0>3} MEM:{1}".format(self.ip_, str(self.mem_)))
            self.clock()
    
    # Function to grab an outputed value       
    def popOutput(self, aIndex = None):
        try:
            if (aIndex == None):
                return self.outBuffer_.pop()
            else:
                return self.outBuffer_.pop(aIndex)
        except:
            return None
    
    # Function to store input value    
    def loadInput(self, aInput):
        self.inBuffer_.append(aInput)
        