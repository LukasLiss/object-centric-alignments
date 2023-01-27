from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Any
from copy import deepcopy


class ObjectCentricPetriNet(object):
    '''
    Storing an Object-Centric Petri Net.


    '''
    class Place(object):
        def __init__(self, name, object_type, out_arcs=None, in_arcs=None, initial=False, final=False, properties=None):
            self.__name = name
            self.__object_type = object_type
            self.__initial = initial
            self.__final = final
            self.__in_arcs = in_arcs if in_arcs != None else set()
            if out_arcs != None:
                self.__out_arcs = out_arcs
            else:
                self.__out_arcs = set()
            self.__properties = dict() if properties is None else properties

        def __set_name(self, name):
            self.__name = name

        def __get_name(self):
            return self.__name

        def __get_object_type(self):
            return self.__object_type

        def __get_initial(self):
            return self.__initial

        def __get_final(self):
            return self.__final

        def __set_final(self, final):
            self.__final = final

        def __get_out_arcs(self):
            return self.__out_arcs

        def __set_out_arcs(self, out_arcs):
            self.__out_arcs = out_arcs

        def __get_in_arcs(self):
            return self.__in_arcs

        def __set_in_arcs(self, in_arcs):
            self.__in_arcs = in_arcs

        def __set_properties(self, properties):
            self.__properties = properties

        def __get_properties(self):
            return self.__properties

        @property
        def preset(self):
            return set([in_arc.source for in_arc in self.__in_arcs])

        @property
        def postset(self):
            return set([out_arc.target for out_arc in self.__out_arcs])

        def __repr__(self):
            return str(self.name)

        def __eq__(self, other):
            # keep the ID for now in places
            return id(self) == id(other)

        def __hash__(self):
            # keep the ID for now in places
            return id(self)

        def __deepcopy__(self, memodict={}):
            new_place = ObjectCentricPetriNet.Place(
                self.name, self.object_type, properties=self.properties, initial=self.initial, final=self.final)
            return new_place

        object_type = property(__get_object_type)
        initial = property(__get_initial)
        final = property(__get_final, __set_final)
        out_arcs = property(__get_out_arcs, __set_out_arcs)
        in_arcs = property(__get_in_arcs, __set_in_arcs)
        name = property(__get_name, __set_name)
        properties = property(__get_properties, __set_properties)

    class Transition(object):
        def __init__(self, name, label=None, in_arcs=None, out_arcs=None, properties=None, silent=False):
            self.__name = name
            self.__label = None if label is None else label
            self.__in_arcs = set() if in_arcs is None else in_arcs
            self.__out_arcs = set() if out_arcs is None else out_arcs
            self.__silent = silent
            self.__properties = dict() if properties is None else properties

        def __set_name(self, name):
            self.__name = name

        def __get_name(self):
            return self.__name

        def __set_label(self, label):
            self.__label = label

        def __get_label(self):
            return self.__label

        def __get_out_arcs(self):
            return self.__out_arcs

        def __get_in_arcs(self):
            return self.__in_arcs

        def __set_properties(self, properties):
            self.__properties = properties

        def __get_properties(self):
            return self.__properties

        def __get_silent(self):
            return self.__silent

        def __set_silent(self, silent):
            self.__silent = silent

        @property
        def preset(self):
            return set([in_arc.source for in_arc in self.__in_arcs])

        @property
        def preset_object_type(self):
            return set([in_arc.source.object_type for in_arc in self.__in_arcs])

        @property
        def postset(self):
            return set([out_arc.target for out_arc in self.__out_arcs])

        @property
        def postset_object_type(self):
            return set([out_arc.target.object_type for out_arc in self.__out_arcs])

        def __repr__(self):
            if self.label is None:
                return str(self.name)
            else:
                return str(self.label)

        def __eq__(self, other):
            # keep the ID for now in transitions
            return id(self) == id(other)

        def __hash__(self):
            # keep the ID for now in transitions
            return id(self)

        def __deepcopy__(self, memodict={}):
            new_trans = ObjectCentricPetriNet.Transition(
                self.name, self.label, properties=self.properties, silent=self.silent)
            return new_trans

        name = property(__get_name, __set_name)
        label = property(__get_label, __set_label)
        in_arcs = property(__get_in_arcs)
        out_arcs = property(__get_out_arcs)
        properties = property(__get_properties, __set_properties)
        silent = property(__get_silent, __set_silent)

    class Arc(object):
        def __init__(self, source, target, variable=False, weight=1, properties=None):
            if type(source) is type(target):
                raise Exception('Petri nets are bipartite graphs!')
            self.__source = source
            self.__target = target
            self.__weight = weight
            self.__variable = variable
            self.__properties = dict() if properties is None else properties

        def __get_source(self):
            return self.__source

        def __set_source(self, source):
            self.__source = source

        def __set_weight(self, weight):
            self.__weight = weight

        def __get_weight(self):
            return self.__weight

        def __get_target(self):
            return self.__target

        def __set_target(self, target):
            self.__target = target

        def __get_variable(self):
            return self.__variable

        def __set_properties(self, properties):
            self.__properties = properties

        def __get_properties(self):
            return self.__properties

        def __repr__(self):
            if type(self.source) is ObjectCentricPetriNet.Transition:
                if self.source.label:
                    return "(t)" + str(self.source.label) + "->" + "(p)" + str(self.target.name)
                else:
                    return "(t)" + str(self.source.name) + "->" + "(p)" + str(self.target.name)
            if type(self.target) is ObjectCentricPetriNet.Transition:
                if self.target.label:
                    return "(p)" + str(self.source.name) + "->" + "(t)" + str(self.target.label)
                else:
                    return "(p)" + str(self.source.name) + "->" + "(t)" + str(self.target.name)

        def __hash__(self):
            return id(self)

        def __eq__(self, other):
            return self.source == other.source and self.target == other.target


        source = property(__get_source, __set_source)
        target = property(__get_target, __set_target)
        variable = property(__get_variable)
        weight = property(__get_weight, __set_weight)
        properties = property(__get_properties, __set_properties)

    def __init__(self, name=None, places=None, transitions=None, arcs=None, properties=None, nets=None):
        self.__name = "" if name is None else name
        self.__places = places if places != None else set()
        self.__transitions = transitions if transitions != None else set()
        self.__arcs = arcs if arcs != None else set()
        self.__properties = dict() if properties is None else properties
        self.__nets = nets if nets is not None else dict()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def places(self):
        '''
        Places of the object-centric Petri net.

        :return: Set of Places
        :rtype: set(Place)
        -------

        '''
        return self.__places

    @property
    def transitions(self):
        '''
        Transitions of the object-centric Petri net.

        :return: Set of Transitions
        :rtype: set(Transition)
        -------

        '''
        return self.__transitions

    @property
    def arcs(self):
        '''
        Arcs of the object-centric Petri net.

        :return: Set of Arcs
        :rtype: set(Arc)
        -------

        '''
        return self.__arcs

    @property
    def properties(self):
        return self.__properties

    @property
    def object_types(self):
        return list(set([pl.object_type for pl in self.__places]))

    @property
    def nets(self):
        return self.__nets

    def add_arc(self, arc):
        '''
        Adds an arc to the object-centric Petri net.
        Parameters
        ----------
        arc: Arc

        Returns
        -------
        None
        '''
        self.__arcs.add(arc)
        arc.source.out_arcs.add(arc)
        arc.target.in_arcs.add(arc)

    def remove_place(self, pl):
        '''
        Removes an already existing place.

        Parameters
        ----------
        pl: Place

        Returns
        -------
        None
        '''
        self.__places.remove(pl)
        remove_arcs = set()
        for arc in self.arcs:
            if arc.source == pl:
                remove_arcs.add(arc)
            elif arc.target == pl:
                remove_arcs.add(arc)
        self.remove_arcs(remove_arcs)

    def remove_arc(self, arc):
        '''
        Removes an already existing arc.

        Parameters
        ----------
        arc: Arc

        Returns
        -------
        None
        '''
        self.__arcs.remove(arc)
        arc.source.out_arcs.remove(arc)
        arc.target.in_arcs.remove(arc)

    def remove_arcs(self, arcs):
        '''
        Removes multiple already existing arcs.

        Parameters
        ----------
        arcs: list(Arc)

        Returns
        -------
        None
        '''
        for arc in arcs:
            self.remove_arc(arc)

    def add_arcs(self, arcs):
        '''
        Adds arcs to the object-centric Petri net.
        Parameters
        ----------
        arcs: list(Arc)

        Returns
        -------

        '''
        for arc in arcs:
            self.add_arc(arc)

    def remove_transition(self, t):
        '''
        Removes an already existing transition from the net.
        Parameters
        ----------
        t: Transition

        Returns
        -------
        None
        '''
        self.__transitions.remove(t)
        remove_arcs = set()
        for arc in self.arcs:
            if arc.source == t:
                remove_arcs.add(arc)
            elif arc.target == t:
                remove_arcs.add(arc)
        self.remove_arcs(remove_arcs)

    def find_arc(self, source, target):
        '''

        Returns an arc object if source and target are connected.
        Soruce and target can not both be transition or both be place.

        Parameters
        ----------
        source: Place or Transition
        target: Place or Transition

        Returns
        -------
        Arc or None
        '''
        for arc in self.__arcs:
            if arc.source == source and arc.target == target:
                return arc
        return None

    def find_transition(self, name):
        '''
        finds a transition by name of the transition.
        Parameters
        ----------
        name: string

        Returns
        -------
        None
        '''
        for transition in self.__transitions:
            if transition.name == name:
                return transition
        return None

    def __deepcopy__(self, memodict={}):
        new_name = deepcopy(self.name)
        new_places = set()
        for old_place in self.places:
            new_place = deepcopy(old_place)
            memodict[id(old_place)] = new_place
            new_places.add(new_place)

        new_transitions = set()
        for old_transition in self.transitions:
            new_transition = deepcopy(old_transition)
            memodict[id(old_transition)] = new_transition
            new_transitions.add(new_transition)

        new_arcs = set()
        for old_arc in self.arcs:
            new_arc = self.Arc(memodict[id(old_arc.source)], memodict[id(old_arc.target)], old_arc.variable,
                               old_arc.weight, old_arc.properties)
            new_arcs.add(new_arc)

        new_properties = deepcopy(self.properties)
        new_nets = deepcopy(self.nets)

        new_ocpn = ObjectCentricPetriNet(name=new_name, places=new_places, transitions=new_transitions,
                                         arcs=None, properties=new_properties, nets=new_nets)
        # add arcs to the petri net
        new_ocpn.add_arcs(new_arcs)

        return new_ocpn


@dataclass
class Marking(object):
    '''
    Representing a Marking of an Object-Centric Petri Net.

    ...

    Attributes
    tokens: set(Tuple)

    Methods
    -------
    add_token(pl, obj):
        adds an object obj to a place pl
    '''
    _tokens: Set[Tuple[ObjectCentricPetriNet.Place, str]
                 ] = field(default_factory=set)

    @property
    def tokens(self) -> Set[Tuple[ObjectCentricPetriNet.Place, str]]:
        return self._tokens

    def add_token(self, pl, obj):
        '''
        Add a token to a place in a marking.
        Parameters
        ----------
        pl: Place
        obj: string

        Returns
        -------
        None

        '''
        temp_tokens = set([(pl, oi) for (pl, oi) in self._tokens if oi == obj])
        self._tokens -= temp_tokens
        self._tokens.add((pl, obj))


@dataclass
class Subprocess(object):
    _ocpn: ObjectCentricPetriNet
    _object_types: Set[str] = field(default_factory=set)
    _activities: Set[str] = field(
        default_factory=set)
    _transitions: Set[ObjectCentricPetriNet.Transition] = field(
        default_factory=set)
    _sound: Any = False

    @property
    def object_types(self) -> Set[str]:
        return self._object_types

    @property
    def transitions(self) -> Set[ObjectCentricPetriNet.Transition]:
        return self._transitions

    @property
    def sound(self):
        return self._sound

    def __post_init__(self):
        if self._object_types != None:
            self._object_types = self._object_types
        else:
            self._object_types = self._ocpn.object_type

        if self._activities != None:
            self._transitions = [self._ocpn.find_transition(
                act) for act in self._activities]

            in_tpl = {tr: [arc.source for arc in tr.in_arcs]
                      for tr in self._transitions}
            out_tpl = {tr: [arc.target for arc in tr.out_arcs]
                       for tr in self._transitions}
            tpl = {tr: in_tpl[tr]+out_tpl[tr] for tr in self._transitions}
            self._sound = True if all(any(
                True if p.object_type in self._object_types else False for p in tpl[tr]) for tr in self._transitions) else False
        else:
            in_tpl = {tr: [arc.source for arc in tr.in_arcs]
                      for tr in self._ocpn.transitions}
            out_tpl = {tr: [arc.target for arc in tr.out_arcs]
                       for tr in self._ocpn.transitions}
            tpl = {tr: in_tpl[tr]+out_tpl[tr] for tr in self._ocpn.transitions}
            self._transitions = list(set(
                [tr for tr in self._ocpn.transitions for p in tpl[tr] if p.object_type in self._object_types]))
            self._sound = True


@dataclass
class EnhancedObjectCentricPetriNet(object):
    ocpn: ObjectCentricPetriNet
    behavior: List[str]
    diagnostics: Dict[str, Any]
