from . import Enum, PersonHelper

class PersonType(Enum):
    """
    Enum that has a single method 'classify' in which it classifies each 
    Person into the three types. Used in PPKind to classify each relation by 
    the kinds of persons participating in it.
    """
    SINGLE = "single"
    DUBLETTE = "dublette"
    VORFIN = "vorfin"


    @classmethod
    def classify(cls, p, strict=True):
        """
        Main classification of a given person.
        
        @param strict: if True, throws an Error if Person is not in singles, dubletten or vorfins. 
        
        --> use strict mode when proceessing relations coming from dubletten (i.e. in re-merge).
        --> disable strict when processing all relations in a vorfin, to catch and process
        the manually created relations that might contain participating Persons outside 
        of our initial de-duplication scope. those are simply classified as singles, because we 
        haven't processed them yet. 
        """
        if p in PersonHelper._singles:
            return PersonType.SINGLE
        elif p in PersonHelper._dubletten:
            return PersonType.DUBLETTE
        elif p in PersonHelper._vorfins:
            return PersonType.VORFIN
        else:
            if strict:
                msg = f"couldn't find type for person {p}({p.id}) {p.__class__.__name__}. Was neither in singles, dubletten nor vorfins"
                PersonHelper.enum_errors["PersonType Classification Error"].append(msg)
                raise Exception(msg)
            else:
                return PersonType.SINGLE

