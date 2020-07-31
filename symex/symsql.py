## This module wraps SQLalchemy's methods to be friendly to
## symbolic / concolic execution.

import fuzzy
import sqlalchemy.orm

oldget = sqlalchemy.orm.query.Query.get
def newget(query, primary_key):
  #print(primary_key)
  pk_name=query.first().__table__.primary_key.columns.keys()[0]
  for i in query.all():
    # j=eval("i.{} == {}".format(pk_name))
    # if j:
    #   return i
    if i.__dict__[pk_name] == primary_key:
      return i
  #print(primary_key == pk_name)
  # primary_key=query.all().first().__table__.primary_key.columns.keys()[0]
  ## Exercise 5: your code here.
  ##
  ## Find the object with the primary key "primary_key" in SQLalchemy
  ## query object "query", and do so in a symbolic-friendly way.
  ##
  ## Hint: given a SQLalchemy row object r, you can find the name of
  ## its primary key using r.__table__.primary_key.columns.keys()[0]
  #exec('return query.filter({} == primary_key}).first()'.format(pk_name))
  return None

sqlalchemy.orm.query.Query.get = newget
