from . import ErrorLoggerMixin, defaultdict, Person, is_dublette

class PersonHelper(ErrorLoggerMixin):
    """
    Helper class that creates the initial sets of persons (singles, dublettten, vorfins).
    
    Adds logic that supports classification of persons, which is handled in PersonType class.
    """
    _singles = []
    _dubletten = []
    _vorfins = []
    _red_groups = []
    
    errors = defaultdict(list)
    enum_errors = defaultdict(list)
    
    
    #@classmethod
    #def calculate_vorfins(cls):
    #    """
    #    Helper to create vorfin set. Redundant with the logic in update_collections, but kept for now.
    #    """
    #    cls._vorfins = Person.objects.filter(name__icontains="vorfin")

    @classmethod
    def get_red_size(cls):
        """
        returns the count of groups of vorfins with red ampel status. Used
        in logging the iteration count.
        """
        return len(cls._red_groups)
    
    @classmethod
    def update_collections(cls):
        """
        Sorts all Persons into vorfin, dubletten and single lists. 
        Throws an error if there is an intersection between the lists.
        """
        vorfins = Person.objects.filter(name__icontains="vorfin")
        dubletten = Person.objects.exclude(personproxy=None)
        dubletten = filter(is_dublette, list(dubletten))
        dubletten = list(dubletten)
        #singles = [el for el in Person.objects.all() if el not in dubletten and el not in vorfins]

        v_set = set(vorfins)
        d_set = set(dubletten)
        p_set = set(Person.objects.all())

        singles = p_set.difference(v_set.union(d_set))
        cls._vorfins = vorfins
        cls._dubletten = dubletten
        cls._singles = singles
        
        test = len(singles)+len(vorfins)+len(dubletten)
        if not Person.objects.count() == test:
            msg = f"Missmatch in collections in PersonHelper. Expected Persons to be split evenly, but got missmatch.\nPersons: {Person.objects.count()}, set union collections: {test}."
            cls.errors["Expectation Missmatch"].append(msg)
            raise Exception(msg)
        
