# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# djfim.contrib.depot

from ..depository import POOL as _POOL, SPACE as _SPACE
from ..runtime import DynamicBlock


class Pool(_POOL):
    '''
    static data object
    '''

    CLASS_GENERATION = 'djfim.contrib.concrete.Generation'
    CLASS_ENTITY     = 'djfim.contrib.concrete.Entity'
    CLASS_LINKAGE    = 'djfim.contrib.depot.Linkage'
    CLASS_DIFF_SOLVER = 'djfim.contrib.diff.DiffScanner'

    def getAHead(self):
        head = None
        try:
            obj = self.STATE_DM.objects.filter(
                imprint__isnull=True
            ).order_by(
                'time_stamp'
            ).last()
            head = self.getGeneration(obj)
        except:
            pass
        return head

    def getBHead(self):
        head = None
        try:
            obj = self.STATE_DM.objects.filter(
                imprint__isnull=False
            ).order_by(
                'time_stamp'
            ).last()
            head = self.getGeneration(obj)
        except:
            pass
        return head

    def getCollection(self, head):
        qset = self.getInternalLinkage().getSet(head)
        return qset

    def getGeneration(self, obj):
        kls = DynamicBlock().getDynClass(self.CLASS_GENERATION)
        return kls(obj, pool=self)

    def getEntity(self, obj):
        kls = DynamicBlock().getDynClass(self.CLASS_ENTITY)
        return kls(obj)

    def getInternalLinkage(self):
        kls = DynamicBlock().getDynClass(self.CLASS_LINKAGE)
        return kls(parent=self)

    def addHead(self, data, aHead=None, bHead=None):
        obj = self.STATE_DM(**data)
        obj.save()
        head = self.getGeneration(obj)

        # link up;
        if aHead:
            #assert head.timestamp >= aHead.timestamp, 'no backdate'
            head.setLink(head.LABEL_LINK_A, aHead.storage_pk, True)
        if bHead:
            #assert head.timestamp >= bHead.timestamp, 'no backdate'
            head.setLink(head.LABEL_LINK_B, bHead.storage_pk, True)
        head.doSave()
        # maybe more generic, but it does not force the derivative to have the specific fields;
        return head

    def addEntity(self, data):
        obj = self.BLOB_DM(**data)
        obj.save()
        return self.getEntity(obj)

    def getDiffSolver(self):
        kls = DynamicBlock().getDynClass(self.CLASS_DIFF_SOLVER)
        return kls

    def getPartitionArguments(self, label):
        arg = {
            'model_name': label,
        }
        return arg


class Linkage(DynamicBlock):
    '''
    internal link encapsulation
    '''

    def __init__(self, parent):
        assert parent is not None, 'invalid value'
        super().__init__()
        self._parent = parent

    @property
    def BLOB_DM(self):
        return self._parent.BLOB_DM

    def get_lookup_arg(self, head):
        d = dict()
        d['entity__generation_id'] = head.storage_pk
        return d

    def getBackingSet(self):
        qset = tuple()
        try:
            qset = self.BLOB_DM.objects.filter(
                **(self._lookup_arg)
            ).distinct()
        except:
            pass
        return qset

    def getSet(self, head):
        self._lookup_arg = self.get_lookup_arg(head)
        return self.getBackingSet()


class WorkSpace(_SPACE):
    '''
    space of live data object
    '''

    CLASS_DATAMODEL_SOLVER = 'djfim.solver.DMSolver'
    CLASS_URI_PARSER = 'djfim.contrib.schema.URIParser'

    def __init__(self):
        super().__init__()
        self.load_preset()

    def load_preset(self):
        self.dm_solver = DynamicBlock().getDynClass(self.CLASS_DATAMODEL_SOLVER)()
        self.uri_solver_kls = DynamicBlock().getDynClass(self.CLASS_URI_PARSER)

        self.storage_pk_field = 'id'
        return self

    def get_live_object(self,  uri):
        '''
        :param uri: (string)
        '''
        obj = None

        d = uri_solver_kls().parseURI(uri)
        try:
            pick_arg = {
                self.storage_pk_field: d['anchor'],
            }
            obj = self.dm_solver.get_model_class(
                d['app_label'],
                d['model_name']
            ).objects.get(**pick_arg)
        except:
            pass
        return obj
