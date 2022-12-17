import copy
from enum import Enum
from env_v3 import EnvironmentManager, SymbolResult
from func_v3 import FunctionManager
from func_v3 import FuncInfo
from intbase import InterpreterBase, ErrorType
from tokenizer import Tokenizer

# Enumerated type for our different language data types
class Type(Enum):
  INT = 1
  BOOL = 2
  STRING = 3
  VOID = 4

  # added for v3
  FUNC = 5 
  OBJ = 6

# Represents a value, which has a type and its value
class Value:
  def __init__(self, type, value = None):
    self.t = type
    self.v = value

  def value(self):
    return self.v

  def set(self, other):
    self.t = other.t
    self.v = other.v

  def type(self):
    return self.t

# Main interpreter class
class Interpreter(InterpreterBase):
  def __init__(self, console_output=True, input=None, trace_output=False):
    super().__init__(console_output, input)
    self._setup_operations()  # setup all valid binary operations and the types they work on
    self._setup_default_values()  # setup the default values for each type (e.g., bool->False)
    self.trace_output = trace_output

  # run a program, provided in an array of strings, one string per line of source code
  def run(self, program):
    self.program = program
    self._compute_indentation(program)  # determine indentation of every line
    self.tokenized_program = Tokenizer.tokenize_program(program)
    self.func_manager = FunctionManager(self.tokenized_program)
    self.ip = self.func_manager.get_function_info(InterpreterBase.MAIN_FUNC).start_ip
    self.return_stack = []
    self.terminate = False
    self.env_manager = EnvironmentManager()   # used to track variables/scope
    # self._resultf_func_info = "" 

    # added for v3:
    # self.func_info = FuncInfo(params, self.ip)

    # main interpreter run loop
    while not self.terminate:
      self._process_line()

  def _process_line(self):
    if self.trace_output:
      print(f"{self.ip:04}: {self.program[self.ip].rstrip()}")
    tokens = self.tokenized_program[self.ip]
    if not tokens:
      self._blank_line()
      return

    args = tokens[1:]

    match tokens[0]:
      case InterpreterBase.ASSIGN_DEF:
        self._assign(args)
      case InterpreterBase.FUNCCALL_DEF:
        self._funccall(args)
      case InterpreterBase.ENDFUNC_DEF:
        self._endfunc()
      case InterpreterBase.IF_DEF:
        self._if(args)
      case InterpreterBase.ELSE_DEF:
        self._else()
      case InterpreterBase.ENDIF_DEF:
        self._endif()
      case InterpreterBase.RETURN_DEF:
        self._return(args)
      case InterpreterBase.WHILE_DEF:
        self._while(args)
      case InterpreterBase.ENDWHILE_DEF:
        self._endwhile(args)
      case InterpreterBase.VAR_DEF: # v2 statements
        self._define_var(args)
      case InterpreterBase.LAMBDA_DEF:
        self._lambda(args)
      case InterpreterBase.ENDLAMBDA_DEF:
        self._endlambda()
      case default:
        raise Exception(f'Unknown command: {tokens[0]}')

  def _blank_line(self):
    self._advance_to_next_statement()

  def _assign(self, tokens):
   if len(tokens) < 2:
     super().error(ErrorType.SYNTAX_ERROR,"Invalid assignment statement")
   vname = tokens[0]
   value_type = self._eval_expression(tokens[1:])
  #  print("value_type: ", value_type.type())

   # if we see a ".", then we know this is an object attribute 
   # that we are trying to assign to something
   # print(self.env_manager.environment)
  #  if "." in tokens[0] and "this" in tokens[0]: 
  #   for env in self.env_manager.environment:
  #     if 
  #   x.value()[] = tokens[1]
  # print(self.env_manager.environment)

   if "." in tokens[0]: 
      # print(self.env_manager.environment)
      list = tokens[0].split(".")
      # print("list: ", list)
      obj = list[0]
      attribute = list[1]
      # print("attribute: ", attribute)
       
      obj = self.env_manager.get(list[0])
      # print("obj value: ", obj.value())
      if obj.type() != Type.OBJ: 
          super().error(ErrorType.TYPE_ERROR,f"{obj} is not of type object", self.ip)
      obj.value()[attribute] = value_type # obj.value() would be the dictionary
      # print("obj value: ", obj.value()[attribute].value())
      self._advance_to_next_statement()

   # otherwise, we are NOT dealing with an object attribute 
   else: 
    existing_value_type = self._get_value(tokens[0])
    # print ("existing_value_type.val(): ", existing_value_type.value())
    # print ("existing_value_type.type(): ", existing_value_type.type())
    
    # assigning function variables and checking if they are functions
    # if existing_value_type.type() == Type.FUNC:
    #   if self.func_manager.is_function(tokens[1]):
    #     self.func_manager.func_cache[tokens[0]] = self.func_manager.func_cache[tokens[1]]

    #   if tokens[1] == "resultf":
    #     # adding resultf to function cache
    #     self.func_manager.func_cache[tokens[1]] = value_type.value()

    if existing_value_type.type() != value_type.type():
      super().error(ErrorType.TYPE_ERROR,
                    f"Trying to assign a variable of {existing_value_type.type()} to a value of {value_type.type()}",
                    self.ip)
    self._set_value(tokens[0], value_type)
    # x, y = self.env_manager.environment[-1][-1][tokens[1]].value()
    # print("func cache value: ", self.func_manager.func_cache)

    # if tokens[1] == "resultf":
    # # # #   # adding resultf to function cache
    #   self.func_manager.func_cache[tokens[0]] = self.func_manager.func_cache[x]
    # print("func cache value: ", self.func_manager.func_cache[tokens[0]].params)
    self._advance_to_next_statement()

  def _lambda(self, args):
    recent_env = self.env_manager.environment[-1][-1]
    lambdas = self.func_manager.create_lambda_name(self.ip)

    self._set_result(Value(Type.FUNC,(lambdas, recent_env)))

    presLine = self.ip + 1
    while len(self.tokenized_program) > presLine :
      if self.indents[presLine] == self.indents[self.ip]:
        if InterpreterBase.ENDLAMBDA_DEF == self.tokenized_program[presLine][0]: 
          self.ip = presLine+1
          return

      if self.indents[self.ip] > self.indents[presLine]:
        if self.tokenized_program[presLine]:
          break
      
      presLine = presLine+1 
    
    super().error(ErrorType.SYNTAX_ERROR,"Endlambda is not there!", self.ip)

  def _endlambda(self): 
    self._endfunc()

  def _funccall(self, args):
    if not args:
      super().error(ErrorType.SYNTAX_ERROR,"Missing function name to call", self.ip)
    if args[0] == InterpreterBase.PRINT_DEF:
      self._print(args[1:])
      self._advance_to_next_statement()
    elif args[0] == InterpreterBase.INPUT_DEF:
      self._input(args[1:])
      self._advance_to_next_statement()
    elif args[0] == InterpreterBase.STRTOINT_DEF:
      self._strtoint(args[1:])
      self._advance_to_next_statement()

    # checks if 
    elif self._get_value(args[0]).type() == Type.FUNC:
      latest_env = self._get_value(args[0]).value()[1]
      actual_name = self._get_value(args[0]).value()[0]
      
      self.return_stack.append(1+self.ip)
      self._create_new_environment(actual_name, args[1:], latest_env)
      self.ip = self._find_first_instruction(actual_name)
    else:
      self.return_stack.append(self.ip+1)
      self._create_new_environment(args[0], args[1:], {})  # Create new environment, copy args into new env
      self.ip = self._find_first_instruction(args[0])

  # create a new environment for a function call
  def _create_new_environment(self, funcname, args, curr_inv):
    formal_params = self.func_manager.get_function_info(funcname)
    # print("cache: ", self.func_manager.func_cache)
    if formal_params is None:
        super().error(ErrorType.NAME_ERROR, f"Unknown function name {funcname}", self.ip)

    if len(formal_params.params) != len(args):
      super().error(ErrorType.NAME_ERROR,f"Mismatched parameter count in call to {funcname}", self.ip)

    tmp_mappings = curr_inv
    for formal, actual in zip(formal_params.params,args):
      formal_name = formal[0]
      formal_typename = formal[1]
      arg = self._get_value(actual)
      if arg.type() != self.compatible_types[formal_typename]:
        super().error(ErrorType.TYPE_ERROR,f"Mismatched parameter type for {formal_name} in call to {funcname}", self.ip)
      if formal_typename in self.reference_types:
        tmp_mappings[formal_name] = arg
      else:
        tmp_mappings[formal_name] = copy.copy(arg)

    # create a new environment for the target function
    # and add our parameters to the env
    self.env_manager.push()
    self.env_manager.import_mappings(tmp_mappings)

  def _endfunc(self, return_val = None):
    if not self.return_stack:  # done with main!
      self.terminate = True
    else:
      self.env_manager.pop()  # get rid of environment for the function
      if return_val:
        self._set_result(return_val)
      else:
        # return default value for type if no return value is specified. Last param of True enables
        # creation of result variable even if none exists, or is of a different type
        return_type = self.func_manager.get_return_type_for_enclosing_function(self.ip)
        if return_type != InterpreterBase.VOID_DEF:
          self._set_result(self.type_to_default[return_type])
      self.ip = self.return_stack.pop()

  def _if(self, args):
    if not args:
      super().error(ErrorType.SYNTAX_ERROR,"Invalid if syntax", self.ip)
    value_type = self._eval_expression(args)
    if value_type.type() != Type.BOOL:
      super().error(ErrorType.TYPE_ERROR,"Non-boolean if expression", self.ip)
    if value_type.value():
      self._advance_to_next_statement()
      self.env_manager.block_nest()  # we're in a nested block, so create new env for it
      return
    else:
      for line_num in range(self.ip+1, len(self.tokenized_program)):
        tokens = self.tokenized_program[line_num]
        if not tokens:
          continue
        if tokens[0] == InterpreterBase.ENDIF_DEF and self.indents[self.ip] == self.indents[line_num]:
          self.ip = line_num + 1
          return
        if tokens[0] == InterpreterBase.ELSE_DEF and self.indents[self.ip] == self.indents[line_num]:
          self.ip = line_num + 1
          self.env_manager.block_nest()  # we're in a nested else block, so create new env for it
          return
    super().error(ErrorType.SYNTAX_ERROR,"Missing endif", self.ip)

  def _endif(self):
    self._advance_to_next_statement()
    self.env_manager.block_unnest()

  # we would only run this if we ran the successful if block, and fell into the else at the end of the block
  # so we need to delete the old top environment
  def _else(self):
    self.env_manager.block_unnest()   # Get rid of env for block above
    for line_num in range(self.ip+1, len(self.tokenized_program)):
      tokens = self.tokenized_program[line_num]
      if not tokens:
        continue
      if tokens[0] == InterpreterBase.ENDIF_DEF and self.indents[self.ip] == self.indents[line_num]:
          self.ip = line_num + 1
          return
    super().error(ErrorType.SYNTAX_ERROR,"Missing endif", self.ip)

  def _return(self,args):
    # do we want to support returns without values?
    return_type = self.func_manager.get_return_type_for_enclosing_function(self.ip)
    default_value_type = self.type_to_default[return_type]
    if default_value_type.type() == Type.VOID:
      if args:
        super().error(ErrorType.TYPE_ERROR,"Returning value from void function", self.ip)
      self._endfunc()  # no return
      return
    if not args:
      self._endfunc()  # return default value
      return

    #otherwise evaluate the expression and return its value
    value_type = self._eval_expression(args)
    if value_type.type() != default_value_type.type():
      super().error(ErrorType.TYPE_ERROR,"Non-matching return type", self.ip)
    self._endfunc(value_type)

  def _while(self, args):
    if not args:
      super().error(ErrorType.SYNTAX_ERROR,"Missing while expression", self.ip)
    value_type = self._eval_expression(args)
    if value_type.type() != Type.BOOL:
      super().error(ErrorType.TYPE_ERROR,"Non-boolean while expression", self.ip)
    if value_type.value() == False:
      self._exit_while()
      return

    # If true, we advance to the next statement
    self._advance_to_next_statement()
    # And create a new scope
    self.env_manager.block_nest()

  def _exit_while(self):
    while_indent = self.indents[self.ip]
    cur_line = self.ip + 1
    while cur_line < len(self.tokenized_program):
      if self.tokenized_program[cur_line][0] == InterpreterBase.ENDWHILE_DEF and self.indents[cur_line] == while_indent:
        self.ip = cur_line + 1
        return
      if self.tokenized_program[cur_line] and self.indents[cur_line] < self.indents[self.ip]:
        break # syntax error!
      cur_line += 1
    # didn't find endwhile
    super().error(ErrorType.SYNTAX_ERROR,"Missing endwhile", self.ip)

  def _endwhile(self, args):
    # first delete the scope
    self.env_manager.block_unnest()
    while_indent = self.indents[self.ip]
    cur_line = self.ip - 1
    while cur_line >= 0:
      if self.tokenized_program[cur_line][0] == InterpreterBase.WHILE_DEF and self.indents[cur_line] == while_indent:
        self.ip = cur_line
        return
      if self.tokenized_program[cur_line] and self.indents[cur_line] < self.indents[self.ip]:
        break # syntax error!
      cur_line -= 1
    # didn't find while
    super().error(ErrorType.SYNTAX_ERROR,"Missing while", self.ip)


  def _define_var(self, args):
    if len(args) < 2:
      super().error(ErrorType.SYNTAX_ERROR,"Invalid var definition syntax", self.ip)
    for var_name in args[1:]:
      if self.env_manager.create_new_symbol(var_name) != SymbolResult.OK:
        super().error(ErrorType.NAME_ERROR,f"Redefinition of variable {args[1]}", self.ip)

      # is the type a valid type?
      if args[0] not in self.type_to_default:
        super().error(ErrorType.TYPE_ERROR,f"Invalid type {args[0]}", self.ip)

      # Create the variable with a copy of the default value for the type
      self.env_manager.set(var_name, copy.deepcopy(self.type_to_default[args[0]]))

    self._advance_to_next_statement()

  def _print(self, args):
    if not args:
      super().error(ErrorType.SYNTAX_ERROR,"Invalid print call syntax", self.ip)
    out = []
    for arg in args:
      val_type = self._get_value(arg)
      out.append(str(val_type.value()))
    super().output(''.join(out))

  def _input(self, args):
    if args:
      self._print(args)
    result = super().get_input()
    self._set_result(Value(Type.STRING, result))   # return always passed back in result

  def _strtoint(self, args):
    if len(args) != 1:
      super().error(ErrorType.SYNTAX_ERROR,"Invalid strtoint call syntax", self.ip)
    value_type = self._get_value(args[0])
    if value_type.type() != Type.STRING:
      super().error(ErrorType.TYPE_ERROR,"Non-string passed to strtoint", self.ip)
    self._set_result(Value(Type.INT, int(value_type.value())))   # return always passed back in result

  def _advance_to_next_statement(self):
    # for now just increment IP, but later deal with loops, returns, end of functions, etc.
    self.ip += 1

  # Set up type-related data structures
  def _setup_default_values(self):
    # set up what value to return as the default value for each type
    self.type_to_default = {}
    self.type_to_default[InterpreterBase.INT_DEF] = Value(Type.INT, 0)
    self.type_to_default[InterpreterBase.STRING_DEF] = Value(Type.STRING, '')
    self.type_to_default[InterpreterBase.BOOL_DEF] = Value(Type.BOOL, False)
    self.type_to_default[InterpreterBase.VOID_DEF] = Value(Type.VOID, None)

    # added for v3
    self.type_to_default[InterpreterBase.FUNC_DEF] = Value(Type.FUNC, ("", {})) # fix the second parameter
    self.type_to_default[InterpreterBase.OBJECT_DEF] = Value(Type.OBJ, {}) # fix the second parameter

    # set up what types are compatible with what other types
    self.compatible_types = {}
    self.compatible_types[InterpreterBase.INT_DEF] = Type.INT
    self.compatible_types[InterpreterBase.STRING_DEF] = Type.STRING
    self.compatible_types[InterpreterBase.BOOL_DEF] = Type.BOOL
    self.compatible_types[InterpreterBase.REFINT_DEF] = Type.INT
    self.compatible_types[InterpreterBase.REFSTRING_DEF] = Type.STRING
    self.compatible_types[InterpreterBase.REFBOOL_DEF] = Type.BOOL
    self.reference_types = {InterpreterBase.REFINT_DEF, Interpreter.REFSTRING_DEF,
                            Interpreter.REFBOOL_DEF}

    # added for v3
    self.compatible_types[InterpreterBase.OBJECT_DEF] = Type.OBJ
    self.compatible_types[InterpreterBase.FUNC_DEF] = Type.FUNC

    # set up names of result variables: resulti, results, resultb
    self.type_to_result = {}
    self.type_to_result[Type.INT] = 'i'
    self.type_to_result[Type.STRING] = 's'
    self.type_to_result[Type.BOOL] = 'b'

    # added for v3: set up names of resultf and resulto
    self.type_to_result[Type.FUNC] = 'f'
    self.type_to_result[Type.OBJ] = 'o'

  # run a program, provided in an array of strings, one string per line of source code
  def _setup_operations(self):
    self.binary_op_list = ['+','-','*','/','%','==','!=', '<', '<=', '>', '>=', '&', '|']
    self.binary_ops = {}
    self.binary_ops[Type.INT] = {
     '+': lambda a,b: Value(Type.INT, a.value()+b.value()),
     '-': lambda a,b: Value(Type.INT, a.value()-b.value()),
     '*': lambda a,b: Value(Type.INT, a.value()*b.value()),
     '/': lambda a,b: Value(Type.INT, a.value()//b.value()),  # // for integer ops
     '%': lambda a,b: Value(Type.INT, a.value()%b.value()),
     '==': lambda a,b: Value(Type.BOOL, a.value()==b.value()),
     '!=': lambda a,b: Value(Type.BOOL, a.value()!=b.value()),
     '>': lambda a,b: Value(Type.BOOL, a.value()>b.value()),
     '<': lambda a,b: Value(Type.BOOL, a.value()<b.value()),
     '>=': lambda a,b: Value(Type.BOOL, a.value()>=b.value()),
     '<=': lambda a,b: Value(Type.BOOL, a.value()<=b.value()),
    }
    self.binary_ops[Type.STRING] = {
     '+': lambda a,b: Value(Type.STRING, a.value()+b.value()),
     '==': lambda a,b: Value(Type.BOOL, a.value()==b.value()),
     '!=': lambda a,b: Value(Type.BOOL, a.value()!=b.value()),
     '>': lambda a,b: Value(Type.BOOL, a.value()>b.value()),
     '<': lambda a,b: Value(Type.BOOL, a.value()<b.value()),
     '>=': lambda a,b: Value(Type.BOOL, a.value()>=b.value()),
     '<=': lambda a,b: Value(Type.BOOL, a.value()<=b.value()),
    }
    self.binary_ops[Type.BOOL] = {
     '&': lambda a,b: Value(Type.BOOL, a.value() and b.value()),
     '==': lambda a,b: Value(Type.BOOL, a.value()==b.value()),
     '!=': lambda a,b: Value(Type.BOOL, a.value()!=b.value()),
     '|': lambda a,b: Value(Type.BOOL, a.value() or b.value())
    }

  def _compute_indentation(self, program):
    self.indents = [len(line) - len(line.lstrip(' ')) for line in program]

  def _find_first_instruction(self, funcname):
    func_info = self.func_manager.get_function_info(funcname)
    if not func_info:
      super().error(ErrorType.NAME_ERROR,f"Unable to locate {funcname} function")

    return func_info.start_ip

  # given a token name (e.g., x, 17, True, "foo"), give us a Value object associated with it
  def _get_value(self, token):
    if not token:
      super().error(ErrorType.NAME_ERROR,f"Empty token", self.ip)
    if token[0] == '"':
      return Value(Type.STRING, token.strip('"'))
    if token.isdigit() or token[0] == '-':
      return Value(Type.INT, int(token))
    if token == InterpreterBase.TRUE_DEF or token == Interpreter.FALSE_DEF:
      return Value(Type.BOOL, token == InterpreterBase.TRUE_DEF)

    # added for v3: check if the token is a function 
    # fix 
    if self.func_manager.is_function(token):
      # func_value = self.func_manager.get_function_info(token)
      return Value(Type.FUNC, (token, {}))

    # added for v3: check if the token is an object
    # fix 

    if "." in token and "this" in token:
      print("env: ", self.env_manager.environment)
      return

    if "." in token:
      list = token.split(".")
      var_name = self.env_manager.get(list[0])

      if var_name.type() != Type.OBJ: 
          super().error(ErrorType.TYPE_ERROR,f"{var_name} is not of type object", self.ip)

      # checking if object attribute is in the object's dictionary 
      if list[1] not in var_name.value():
        super().error(ErrorType.NAME_ERROR,f"No object of attribute, '{list[1]}', exists", self.ip)
      return var_name.value()[list[1]]

    # look in environments for variable
    val = self.env_manager.get(token) 
    if val != None:
      return val
    # not found
    super().error(ErrorType.NAME_ERROR,f"Unknown variable {token}", self.ip)

  # given a variable name and a Value object, associate the name with the value
  def _set_value(self, varname, to_value_type):
    value_type = self.env_manager.get(varname)
    # print("val object: ", value_type)
    # print("val object type: ", value_type.type())
    # print("val object val: ", value_type.value())

    if value_type == None:
      super().error(ErrorType.NAME_ERROR,f"Assignment of unknown variable {varname}", self.ip)
    value_type.set(to_value_type)

  # bind the result[s,i,b] variable in the calling function's scope to the proper Value object
  def _set_result(self, value_type):
    # always stores result in the highest-level block scope for a function, so nested if/while blocks
    # don't each have their own version of result
    result_var = InterpreterBase.RESULT_DEF + self.type_to_result[value_type.type()]

    self.env_manager.create_new_symbol(result_var, True)  # create in top block if it doesn't exist
    # print("environment of result: ", self.env_manager.environment)
    # print("value: ", value_type.value())
    # print("type: ", value_type.type())
    self.env_manager.set(result_var, copy.deepcopy(value_type))
    # print("env: ", self.env_manager.environment)
    #print("environment of result after: ", self.env_manager.environment)

  # evaluate expressions in prefix notation: + 5 * 6 x
  def _eval_expression(self, tokens):
    stack = []

    for token in reversed(tokens):
      if token in self.binary_op_list:
        v1 = stack.pop()
        v2 = stack.pop()
        if v1.type() != v2.type():
          super().error(ErrorType.TYPE_ERROR,f"Mismatching types {v1.type()} and {v2.type()}", self.ip)
        operations = self.binary_ops[v1.type()]
        if token not in operations:
          super().error(ErrorType.TYPE_ERROR,f"Operator {token} is not compatible with {v1.type()}", self.ip)
        stack.append(operations[token](v1,v2))
      elif token == '!':
        v1 = stack.pop()
        if v1.type() != Type.BOOL:
          super().error(ErrorType.TYPE_ERROR,f"Expecting boolean for ! {v1.type()}", self.ip)
        stack.append(Value(Type.BOOL, not v1.value()))
      else:
        value_type = self._get_value(token)
        stack.append(value_type)

    if len(stack) != 1:
      super().error(ErrorType.SYNTAX_ERROR,f"Invalid expression", self.ip)

    return stack[0]
