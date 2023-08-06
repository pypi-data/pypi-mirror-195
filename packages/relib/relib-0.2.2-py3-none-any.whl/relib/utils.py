from typing import TypeVar, Any

# TODO: make generic for list and set etc (abc.Sequence?)

T = TypeVar('T')
U = TypeVar('U')

def list_split(l: list[T | U], sep: U) -> list[list[T]]:
  l = [sep, *l, sep]
  split_at = [i for i, x in enumerate(l) if x is sep]
  ranges = list(zip(split_at[0:-1], split_at[1:]))
  result: Any = [
    l[start + 1:end]
    for start, end in ranges
  ]
  return result

def drop_none(l: list[T | None]) -> list[T]:
  return [x for x in l if x is not None]

def distinct(items: list[T]) -> list[T]:
  return list(set(items))

def find(iterable):
  return next(iterable, None)

def transpose_dict(des):
  if isinstance(des, list):
    keys = list(des[0].keys()) if des else []
    length = len(des)
    return {
      key: [des[i][key] for i in range(length)]
      for key in keys
    }
  elif isinstance(des, dict):
    keys = list(des.keys())
    length = len(des[keys[0]]) if keys else 0
    return [
      {key: des[key][i] for key in keys}
      for i in range(length)
    ]
  raise ValueError('transpose_dict only accepts dict or list')

def make_combinations_by_dict(des, keys=None, pairs=[]):
  keys = sorted(des.keys()) if keys == None else keys
  if len(keys) == 0:
    return [dict(pairs)]
  key = keys[0]
  remaining_keys = keys[1:]
  new_pairs = [(key, val) for val in des[key]]
  return flatten([
    make_combinations_by_dict(des, remaining_keys, [pair] + pairs)
    for pair in new_pairs
  ])

def merge_dicts(*dicts):
  result = {}
  for dictionary in dicts:
    result.update(dictionary)
  return result

def intersect(*lists: list[T]) -> list[T]:
  return set.intersection(*map(set, lists))

# TODO
def ensure_tuple(value):
  if isinstance(value, tuple):
    return value
  return (value,)

# TODO
def omit(d, keys):
  if keys:
    d = dict(d)
    for key in keys:
      del d[key]
  return d

# TODO
def tuple_by(d, keys):
  return tuple(d[key] for key in keys)

def flatten(l: list[list[T]]) -> list[T]:
  return [value for inner_list in l for value in inner_list]

# TODO?
def transpose(tuples, default_num_returns=0):
  result = tuple(zip(*tuples))
  if not result:
    return ([],) * default_num_returns
  return tuple(map(list, result))

def deepen_dict(d):
  result = {}
  for (*tail, head), value in d.items():
    curr = result
    for key in tail:
      if key not in curr:
        curr[key] = {}
      curr = curr[key]
    curr[head] = value
  return result

# TODO
def group(pairs):
  values_by_key = {}
  for key, value in pairs:
    if key not in values_by_key:
      values_by_key[key] = []
    values_by_key[key].append(value)
  return values_by_key

def get_at(d, keys, default):
  try:
    for key in keys:
      d = d[key]
  except KeyError:
    return default
  return d
