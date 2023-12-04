import copy
import logging
import pygame
logging.basicConfig(level=logging.DEBUG)

class UID:
    uid = 0
    def genUID() -> int:
        UID.uid += 1
        return UID.uid

class Component:
    def __init__(self) -> None:
        self.tags = []
        self.parent = None
        self.id()
    def id(self,id = -1):
        if id == -1:
            self.uid = UID.genUID()
        else:
            self.uid = id
        return self
    def tag(self,*tags):
        self.tags.extend(tags)
        return self
    def ready(self):
        if self.parent:
            self.transform = self.parent.transform
    def get_siblings(self,type):
        return self.get_parent().get_components(type)
    def duplicate(self):
        return copy.copy(self).id()
    def back(self):
        return self.parent
    def set(self,field,apply):
        if hasattr(self,field):
            f =  getattr(self,field)
            if callable(apply):
                apply(f)
            else:
               f = apply
               logging.debug(f'set {self}::{field} from {f} to {apply}')
        else:
            raise AttributeError(f'{type(self)} :: {field} not found')
        return self
    
class Vec2(pygame.math.Vector2):pass
class Transform2D(Component):
    def __init__(self) -> None:
        super().__init__()
        self.setup()
    def setup(self,pos=Vec2(0,0),rot=0.0,scale=Vec2(1,1)):
        self.position = pos
        self.rotation = rot
        self.scale = scale
        return self

class Entity(Component):
    def __init__(self,*components):
        super().__init__()
        self.components = {}
        self.add(*components)
        if not self.has_component(Transform2D):
            self.transform = Transform2D()
            self.add(self.transform)
        else:
            self.transform = self.get_component(Transform2D)
        self.query = Query(self)
    def add(self,*components):
        for component in components:
            if isinstance(component,Component):
                component_type = type(component)
                if component_type not in self.components:
                    self.components[component_type] = []
                self.components[component_type].append(component)
                component.parent = self
            else:
                raise TypeError('must be a componet instance')
        return self
    
    def duplicate(self):
        duplicate_entity = Entity()
        duplicate_entity.components={}
        for component_type, components in self.components.items():
            for component in components:
                duplicate_component = component.duplicate()
                if duplicate_component:
                    duplicate_component.parent = duplicate_entity
                    duplicate_component.transform = duplicate_entity.transform
                    duplicate_entity.add(duplicate_component)
                    duplicate_component.ready()
        return duplicate_entity
    
    def get_component(self, component_type):
        components = self.components.get(component_type, [])
        if len(components) == 1:
            return components[0]
        else:
            return None
    def get_components(self,type):
        return Group(self.components.get(type,[]))
    
    def has_component(self,type):
        return bool(len(self.get_components(type).unpack())> 0)
    def remove_component(self, component_type):
        if component_type in self.components:
            components = self.components[component_type]
            if components:
                removed_component = components.pop()
                removed_component.parent = None
                return True
        return False
    
    def call_all(self, fn=''):
        for type,comps in self.components.items():
            if hasattr(type,fn):
                func = getattr(type,fn)
                for comp in comps:
                    func(comp)
        return self
    def ready(self):
        self.call_all('ready')
        return self
    def update(self):
        self.call_all('update')
        return self

class Group:
    def __init__(self, *members) -> None:
        self.members = []
        self.members.extend(*members)
    def single(self):
        if len(self.members) > 1:
            raise Warning('It has not just one component')
        return self.members[0]
    def unpack(self):
        return self.members
    
class Query:
    def __init__(self, entity):
        self.entity = entity
        self.query_types = []
        self.with_components = []
        self.without_components = []
        self.result = []
    
    def of(self, *types):
        self.with_components=[]
        self.without_components =[]
        self.query_types = []
        self.query_types.extend(types)
        return self

    def has(self, *components):
        self.with_components.extend(components)
        return self

    def no(self, *components):
        self.without_components.extend(components)
        return self

    def exec(self):
        if len(self.query_types) == 0:
            self.query_types.append(Entity)
        self.result = [
            sub_entity
            for query_type in self.query_types
            for sub_entity in self.entity.get_components(query_type).unpack()
            if all( sub_entity.has_component(type) for type in self.with_components)
            and all( not sub_entity.has_component(type) for type in self.without_components)
        ]
        return self
    
    def once(self,fn):
        [fn(entity) for entity in self.exec().result]
        return self
    
class Scene(Entity): pass

class Self:pass
class Modifier(Component):
    def __init__(self,type) -> None:
        super().__init__()
        self.target = type
    def mod(self,modFn):
        self.modFn = modFn
        return self
    def ready(self):
        if self.target == Self:
            self.its =[]
            self.its.append(self.parent)
        else:
            self.its = self.parent.query.of(self.target).exec().result
    def duplicate(self):
        return None
class Update(Modifier):
    def update(self):
        for it in self.its:
            self.modFn(it)
class Ready(Modifier):
    def ready(self):
        super().ready()
        for it in self.its:
            self.modFn(it)

'''
elif issubclass(component,Component):
                parameters = inspect.signature(component).parameters
                if len(parameters) > 0:
                    raise KeyError("Creation needs parameters::",parameters,component)
                component_type = component
                if component_type not in self.components:
                    self.components[component_type] = []
                instance = component_type()
                instance.parent = self
                self.components[component_type].append(instance)
'''
