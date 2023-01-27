from localocpa.objects.oc_petri_net.obj import ObjectCentricPetriNet

class TestOCPNS:
    def __init__(self):
        pass

    def nue_net_required(self):
        ocpn = ObjectCentricPetriNet(name="Nue-Net")

        p1 = ObjectCentricPetriNet.Place(name="p1", object_type="GIFT", initial=True)
        ocpn.places.add(p1)
        p2 = ObjectCentricPetriNet.Place(name="p2", object_type="GIFT")
        ocpn.places.add(p2)
        p3 = ObjectCentricPetriNet.Place(name="p3", object_type="GIFT")
        ocpn.places.add(p3)
        p4 = ObjectCentricPetriNet.Place(name="p4", object_type="GIFT")
        ocpn.places.add(p4)
        p5 = ObjectCentricPetriNet.Place(name="p5", object_type="GIFT", final=True)
        ocpn.places.add(p5)

        t1 = ObjectCentricPetriNet.Transition(name="Receive Material", label="Receive Material")
        ocpn.transitions.add(t1)
        t2 = ObjectCentricPetriNet.Transition(name="Premium Packaging", label="Premium Packaging")
        ocpn.transitions.add(t2)
        t3 = ObjectCentricPetriNet.Transition(name="Premium Ribbon", label="Premium Ribbon")
        ocpn.transitions.add(t3)
        t4 = ObjectCentricPetriNet.Transition(name="Standard Packaging", label="Standard Packaging")
        ocpn.transitions.add(t4)
        t5 = ObjectCentricPetriNet.Transition(name="Standard Ribbon", label="Standard Ribbon")
        ocpn.transitions.add(t5)

        ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, t1, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p2, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p2, t2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p2, t4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t2, p3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t4, p4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p4, t5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t3, p5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t5, p5))

        return ocpn, "sample-logs/jsonocel/nue-net.jsonocel"

    def inter_object_dependencies(self):
        ocpn = ObjectCentricPetriNet(name="Inter Object Dependecies Net")

        p1 = ObjectCentricPetriNet.Place(name="p1", object_type="O", initial=True)
        ocpn.places.add(p1)
        p2 = ObjectCentricPetriNet.Place(name="p2", object_type="I", initial=True)
        ocpn.places.add(p2)
        p3 = ObjectCentricPetriNet.Place(name="p3", object_type="O")
        ocpn.places.add(p3)
        p4 = ObjectCentricPetriNet.Place(name="p4", object_type="I")
        ocpn.places.add(p4)
        p5 = ObjectCentricPetriNet.Place(name="p5", object_type="O")
        ocpn.places.add(p5)
        p6 = ObjectCentricPetriNet.Place(name="p6", object_type="O")
        ocpn.places.add(p6)
        p7 = ObjectCentricPetriNet.Place(name="p7", object_type="I")
        ocpn.places.add(p7)
        p8 = ObjectCentricPetriNet.Place(name="p8", object_type="I")
        ocpn.places.add(p8)
        p9 = ObjectCentricPetriNet.Place(name="p9", object_type="O")
        ocpn.places.add(p9)
        p10 = ObjectCentricPetriNet.Place(name="p10", object_type="O")
        ocpn.places.add(p10)
        p11 = ObjectCentricPetriNet.Place(name="p11", object_type="I")
        ocpn.places.add(p11)
        p12 = ObjectCentricPetriNet.Place(name="p12", object_type="I")
        ocpn.places.add(p12)
        p13 = ObjectCentricPetriNet.Place(name="p13", object_type="O", final=True)
        ocpn.places.add(p13)
        p14 = ObjectCentricPetriNet.Place(name="p14", object_type="I", final=True)
        ocpn.places.add(p14)

        t1 = ObjectCentricPetriNet.Transition(name="s", label="s")
        ocpn.transitions.add(t1)
        t2 = ObjectCentricPetriNet.Transition(name="a", label="a")
        ocpn.transitions.add(t2)
        t3 = ObjectCentricPetriNet.Transition(name="k", label="k")
        ocpn.transitions.add(t3)
        t4 = ObjectCentricPetriNet.Transition(name="c", label="c")
        ocpn.transitions.add(t4)
        t5 = ObjectCentricPetriNet.Transition(name="m", label="m")
        ocpn.transitions.add(t5)
        t6 = ObjectCentricPetriNet.Transition(name="b", label="b")
        ocpn.transitions.add(t6)
        t7 = ObjectCentricPetriNet.Transition(name="l", label="l")
        ocpn.transitions.add(t7)
        t8 = ObjectCentricPetriNet.Transition(name="d", label="d")
        ocpn.transitions.add(t8)
        t9 = ObjectCentricPetriNet.Transition(name="n", label="n")
        ocpn.transitions.add(t9)
        t10 = ObjectCentricPetriNet.Transition(name="e", label="e")
        ocpn.transitions.add(t10)
        t11 = ObjectCentricPetriNet.Transition(name="o", label="o")
        ocpn.transitions.add(t11)

        ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, t1))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p2, t1))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p4, t4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p4, t5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t2, p5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t3, p6))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t4, p7))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t5, p8))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p5, t6))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p6, t7))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p7, t8))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p8, t9))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t6, p9))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t7, p10))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t8, p11))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t9, p12))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p9, t10))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p10, t11))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p11, t10))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p12, t11))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t10, p13))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t10, p14))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t11, p13))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t11, p14))

        return ocpn, "sample-logs/jsonocel/inter-object-dependencies.jsonocel"

    def seperate_object_instances(self):
        ocpn = ObjectCentricPetriNet(name="Seperate Object Instances")

        p1 = ObjectCentricPetriNet.Place(name="p1", object_type="O", initial=True)
        ocpn.places.add(p1)
        p2 = ObjectCentricPetriNet.Place(name="p2", object_type="O")
        ocpn.places.add(p2)
        p3 = ObjectCentricPetriNet.Place(name="p3", object_type="O")
        ocpn.places.add(p3)
        p4 = ObjectCentricPetriNet.Place(name="p4", object_type="O")
        ocpn.places.add(p4)
        p5 = ObjectCentricPetriNet.Place(name="p5", object_type="O")
        ocpn.places.add(p5)
        p6 = ObjectCentricPetriNet.Place(name="p6", object_type="O", final=True)
        ocpn.places.add(p6)

        t1 = ObjectCentricPetriNet.Transition(name="r", label="r")
        ocpn.transitions.add(t1)
        t2 = ObjectCentricPetriNet.Transition(name="p", label="p")
        ocpn.transitions.add(t2)
        t3 = ObjectCentricPetriNet.Transition(name="a", label="a")
        ocpn.transitions.add(t3)
        t4 = ObjectCentricPetriNet.Transition(name="s", label="s")
        ocpn.transitions.add(t4)

        ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, t1, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p2, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p3, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p2, t2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t2, p4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t3, p5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p4, t4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p5, t4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t4, p6))

        return ocpn, "sample-logs/jsonocel/seperate-object-identities.jsonocel"

    def running_example(self):
        ocpn = ObjectCentricPetriNet(name="Running Example")

        p1 = ObjectCentricPetriNet.Place(name="p1", object_type="Package", initial=True)
        ocpn.places.add(p1)
        p2 = ObjectCentricPetriNet.Place(name="p2", object_type="Package")
        ocpn.places.add(p2)
        p3 = ObjectCentricPetriNet.Place(name="p3", object_type="Package")
        ocpn.places.add(p3)
        p4 = ObjectCentricPetriNet.Place(name="p4", object_type="Package")
        ocpn.places.add(p4)
        p5 = ObjectCentricPetriNet.Place(name="p5", object_type="Package")
        ocpn.places.add(p5)
        p6 = ObjectCentricPetriNet.Place(name="p6", object_type="Package", final=True)
        ocpn.places.add(p6)

        pi1 = ObjectCentricPetriNet.Place(name="pi1", object_type="Item", initial=True)
        ocpn.places.add(pi1)
        pi2 = ObjectCentricPetriNet.Place(name="pi2", object_type="Item")
        ocpn.places.add(pi2)
        pi3 = ObjectCentricPetriNet.Place(name="pi3", object_type="Item")
        ocpn.places.add(pi3)
        pi4 = ObjectCentricPetriNet.Place(name="pi4", object_type="Item")
        ocpn.places.add(pi4)
        pi5 = ObjectCentricPetriNet.Place(name="pi5", object_type="Item")
        ocpn.places.add(pi5)
        pi6 = ObjectCentricPetriNet.Place(name="pi6", object_type="Item", final=True)
        ocpn.places.add(pi6)

        t1 = ObjectCentricPetriNet.Transition(name="receive sample order", label="receive sample order")
        ocpn.transitions.add(t1)
        t2 = ObjectCentricPetriNet.Transition(name="setup envelope", label="setup envelope")
        ocpn.transitions.add(t2)
        t3 = ObjectCentricPetriNet.Transition(name="setup box", label="setup box")
        ocpn.transitions.add(t3)
        t4 = ObjectCentricPetriNet.Transition(name="add advertisement", label="add advertisement")
        ocpn.transitions.add(t4)
        t5 = ObjectCentricPetriNet.Transition(name="add bill", label="add bill")
        ocpn.transitions.add(t5)

        ti1 = ObjectCentricPetriNet.Transition(name="receive product order", label="receive product order")
        ocpn.transitions.add(ti1)
        ti2 = ObjectCentricPetriNet.Transition(name="note sample number", label="note sample number")
        ocpn.transitions.add(ti2)
        ti3 = ObjectCentricPetriNet.Transition(name="note product number", label="note product number")
        ocpn.transitions.add(ti3)
        ti4 = ObjectCentricPetriNet.Transition(name="add sample", label="add sample")
        ocpn.transitions.add(ti4)
        ti5 = ObjectCentricPetriNet.Transition(name="add product", label="add product")
        ocpn.transitions.add(ti5)

        ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, t1))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, ti1))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi1, t1, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi1, ti1, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, pi2, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti1, p3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti1, pi3, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p2, t2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi2, ti2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi3, ti3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t2, p4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t3, p5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti2, pi4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti3, pi5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p4, t4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p5, t5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi4, ti4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi5, ti5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t4, p6))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t5, p6))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti4, pi6))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti5, pi6))

        return ocpn, "sample-logs/jsonocel/running-example.jsonocel"

    def paper_example(self):
        ocpn = ObjectCentricPetriNet(name="Running Example")

        p1 = ObjectCentricPetriNet.Place(name="p1", object_type="Package", initial=True)
        ocpn.places.add(p1)
        p2 = ObjectCentricPetriNet.Place(name="p2", object_type="Package")
        ocpn.places.add(p2)
        p3 = ObjectCentricPetriNet.Place(name="p3", object_type="Package")
        ocpn.places.add(p3)
        p4 = ObjectCentricPetriNet.Place(name="p4", object_type="Package")
        ocpn.places.add(p4)
        p5 = ObjectCentricPetriNet.Place(name="p5", object_type="Package")
        ocpn.places.add(p5)
        p6 = ObjectCentricPetriNet.Place(name="p6", object_type="Package", final=True)
        ocpn.places.add(p6)

        pi1 = ObjectCentricPetriNet.Place(name="pi1", object_type="Item", initial=True)
        ocpn.places.add(pi1)
        pi2 = ObjectCentricPetriNet.Place(name="pi2", object_type="Item")
        ocpn.places.add(pi2)
        pi3 = ObjectCentricPetriNet.Place(name="pi3", object_type="Item")
        ocpn.places.add(pi3)
        pi4 = ObjectCentricPetriNet.Place(name="pi4", object_type="Item")
        ocpn.places.add(pi4)
        pi5 = ObjectCentricPetriNet.Place(name="pi5", object_type="Item")
        ocpn.places.add(pi5)
        pi6 = ObjectCentricPetriNet.Place(name="pi6", object_type="Item", final=True)
        ocpn.places.add(pi6)

        t1 = ObjectCentricPetriNet.Transition(name="receive sample order", label="receive sample order")
        ocpn.transitions.add(t1)
        t2 = ObjectCentricPetriNet.Transition(name="setup envelope", label="setup envelope")
        ocpn.transitions.add(t2)
        t3 = ObjectCentricPetriNet.Transition(name="setup box", label="setup box")
        ocpn.transitions.add(t3)
        t4 = ObjectCentricPetriNet.Transition(name="add advertisement", label="add advertisement")
        ocpn.transitions.add(t4)
        t5 = ObjectCentricPetriNet.Transition(name="add bill", label="add bill")
        ocpn.transitions.add(t5)

        ti1 = ObjectCentricPetriNet.Transition(name="receive product order", label="receive product order")
        ocpn.transitions.add(ti1)
        ti2 = ObjectCentricPetriNet.Transition(name="prepare sample", label="prepare sample")
        ocpn.transitions.add(ti2)
        ti3 = ObjectCentricPetriNet.Transition(name="prepare product", label="prepare product")
        ocpn.transitions.add(ti3)
        ti4 = ObjectCentricPetriNet.Transition(name="add sample", label="add sample")
        ocpn.transitions.add(ti4)
        ti5 = ObjectCentricPetriNet.Transition(name="add product", label="add product")
        ocpn.transitions.add(ti5)

        ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, t1))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, ti1))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi1, t1, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi1, ti1, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, pi2, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti1, p3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti1, pi3, variable=True))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p2, t2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi2, ti2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi3, ti3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t2, p4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t3, p5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti2, pi4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti3, pi5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p4, t4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p5, t5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi4, ti4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(pi5, ti5))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t4, p6))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t5, p6))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti4, pi6))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(ti5, pi6))

        return ocpn, "sample-logs/jsonocel/paper-example.jsonocel"

    def silent_transitions(self):
        ocpn = ObjectCentricPetriNet(name="Silent Transition")

        p1 = ObjectCentricPetriNet.Place(name="p1", object_type="O", initial=True)
        ocpn.places.add(p1)
        p2 = ObjectCentricPetriNet.Place(name="p2", object_type="O")
        ocpn.places.add(p2)
        p3 = ObjectCentricPetriNet.Place(name="p3", object_type="O")
        ocpn.places.add(p3)
        p4 = ObjectCentricPetriNet.Place(name="p4", object_type="O", final=True)
        ocpn.places.add(p4)

        t1 = ObjectCentricPetriNet.Transition(name="a", label="a")
        ocpn.transitions.add(t1)
        t2 = ObjectCentricPetriNet.Transition(name="b", label="b")
        ocpn.transitions.add(t2)
        t3 = ObjectCentricPetriNet.Transition(name="c", label="c")
        ocpn.transitions.add(t3)
        t_silent = ObjectCentricPetriNet.Transition(name="s", label="s", silent=True)
        ocpn.transitions.add(t_silent)

        ocpn.add_arc(ObjectCentricPetriNet.Arc(p1, t1))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t1, p2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p2, t2))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t2, p3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t3))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t3, p4))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(p3, t_silent))
        ocpn.add_arc(ObjectCentricPetriNet.Arc(t_silent, p2))

        return ocpn, "sample-logs/jsonocel/silent_transitions.jsonocel"
