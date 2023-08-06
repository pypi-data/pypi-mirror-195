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
# djfim.contrib.action

import json

from django.utils import timezone

from dmprj.engineering.versioncontrol.actions import VersionControlAction,  BLEND as _LOAD,  CAPTURE as _SAVE,  DISTILL as _DUMP

from ..runtime import DynamicBlock


class LOAD(_LOAD):

    def __init__(self,  pool=None, image=None):
        assert pool is not None,  'invalid value'
        assert image is not None,  'invalid value'
        super().__init__()
        self._pool = pool
        self._image = image

    def main_play(self):
        # a) get head;
        self._pool.getBHead()
        # b) load in data;
        return None


class EXPORT(_DUMP):

    def __init__(self,  pool=None, image=None):
        assert pool is not None,  'invalid value'
        assert image is not None,  'invalid value'
        super().__init__()
        self._pool = pool
        self._image = image

    def prologue(self):
        # a) get head;
        self._head = self._pool.getBHead()
        assert self._head is not None, 'no data to file out'
        return self

    def dumpHeadAsString(self, head):
        rval = head.toBIEF() + '\n'
        return rval

    def dumpEntityAsString(self, entity):
        rval = entity.toBIEF() + '\n'
        return rval

    def main_play(self):
        # b) write out data;
        with open(self._image, 'w') as _out:
            _out.write(self.dumpHeadAsString(self._head))
            _out.write('\n')
            for item in self._head.getEntitySet():
                _out.write(self.dumpEntityAsString(item))
                _out.write('\n')
        return None


class SAVE(_SAVE):

    def __init__(self, context, pool=None, wspace=None, memo=''):
        assert pool is not None,  'invalid value'
        assert wspace is not None,  'invalid value'
        super().__init__()
        self._context = context
        self._pool = pool
        self._wspace = wspace
        self._memo = memo

    def prologue(self):
        self._collect_cache = self._context.getActionCache()
        # a) get head;
        self._a_head = self._pool.getAHead()
        return self

    def main_play(self):
        self._ts = timezone.now()
        # b) collect data;
        self.doCapture(a_head=self._a_head)
        return self

    def epilogue(self):
        # c) do posthook;
        digest_kls = self._context.getDigestSolver()
        digest_kls(self._new_head).updateNode()

        imprint_kls = self._context.getImprintSolver()
        imprint_kls(self._new_head).updateNode()
        return self

    def constructNode(self):
        ss_digest = ''
        ss_imprint = None

        node = {
            'time_stamp': self._ts,
            'digest': ss_digest,
            'imprint': ss_imprint,
            'memo': self._memo,
        }
        return node

    def collectObject(self):
        catalog = self._context.getSortSolver().get()
        for item in catalog:
            extractor = self._context.getExtractor(item)
            extractor.do(cache=self._collect_cache, head=self._new_head)
        return self

    def storeBlob(self):
        archiver = self._context.getArchiver()
        for item in self._collect_cache:
            archiver.setHead(self._new_head)
            archiver.doArchive(item)
        return self

    def doCapture(self, a_head):
        item = self.constructNode()
        self._new_head = self._pool.addHead(
            item,
            aHead=self._a_head
        )

        self.collectObject()
        self.storeBlob()
        return self


class FIXUP(VersionControlAction):
    CLASS_DIFF_SCANNER = 'djfim.contrib.diff.DiffScanner'
    CLASS_DIFF_LOADER  = 'djfim.contrib.diff.DiffLoader'
    CLASS_DIFF_ACTOR  = 'djfim.contrib.diff.DiffActuator'

    def __init__(self, context, pool=None, wspace=None,  hint=None):
        assert pool is not None,  'invalid value'
        assert wspace is not None,  'invalid value'
        super().__init__()
        self._context = context
        self._pool = pool
        self._wspace = wspace
        self._hint = hint

    def prologue(self):
        self.storage_pk_field = 'id'
        return self

    def main_play(self):
        if self._hint is None:
            self.generateHint()
            self._hint = self.get_hint_content()
        else:
            self.readHintAndApply()
        return self

    def generateHint(self):
        self._cache = list()
        # a) get heads;
        self.a_head = self._pool.getAHead()
        self.b_head = self._pool.getBHead()
        # b) compare data;
        scanner_cls = DynamicBlock().getDynClass(self.CLASS_DIFF_SCANNER)
        scanner = scanner_cls(
            self._context,
            self.a_head,
            self.b_head
        )
        scanner.getDiff(sink=self._cache)
        return self

    def get_hint_content(self):
        full = {
            '_meta': {
                'a': self.a_head.storage_pk,
                'b': self.b_head.storage_pk,
            },
            'diff': [ x.asDict() for x in self._cache ],
        }
        return json.dumps(full)

    def updateSpace(self, wspace, item):
        live_obj = self._wspace.get_live_object(item.uri)
        if live_obj is None:
            self.createNewObj(item)
        else:
            self.updateLiveObj(live_obj, item)
        return self

    def updateLiveObj(self, obj, item):
        for k, v in item.copyAsDict():
            if k in (self.storage_pk_field,):
                continue
            setattr(obj, k, v)
        obj.save()
        return self

    def createNewObj(self, item):
        obj_dm = self.dm_solver.get_model_class()
        new_obj = obj_dm(**(item.copyAsDict()))
        new_obj.save()
        setattr(item._obj, 'anchor', new_obj.id)
        item.doSave()
        return self

    def readHintAndApply(self):
        # a) get heads;
        self.a_head = self._pool.getAHead()
        self.b_head = self._pool.getBHead()
        # b) combine data;
        diff_loader = DynamicBlock().getDynClass(self.CLASS_DIFF_LOADER)
        diff_actor = DynamicBlock().getDynClass(self.CLASS_DIFF_ACTOR)
        actor = diff_actor(
            self.a_head,
            self.b_head,
            diff_loader().loadFromString(self._hint)
        )
        actor.do(now=timezone.now())
        # c) apply to live objs;
        for item in actor.latest_head.getCollection():
            self.updateSpace(self._wspace, item)
        return self
