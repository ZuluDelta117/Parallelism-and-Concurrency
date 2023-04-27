"""
Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04

Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')

10% Bonus to speed up part 3
"""
from common import *
from multiprocessing.pool import ThreadPool

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):

    if family_id == None:
        return

    # print(f'Retrieving Family: {family_id}')

    # Call Family API via thread
    req_family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    req_family.start()
    req_family.join()

    new_family = Family(family_id, req_family.response)
    tree.add_family(new_family)

    # Get husband details
    husband_id, wife_id, children_ids = new_family.husband, new_family.wife, [c for c in new_family.children if not tree.does_person_exist(c)]
    
    # print(f'   Retrieving Husband : {husband_id}')
    # print(f'   Retrieving Wife    : {wife_id}')
    # print(f'   Retrieving children: {str(children_ids)[1:-1]}')
    
    # create parent thread calling API to get parent data
    req_parents = [Request_thread(f'{TOP_API_URL}/person/{id}') for id in [husband_id, wife_id]]
    
    # start all parent threads
    for t in req_parents:
        t.start()
    
    # Join all parent threads
    for t in req_parents:
        t.join()
    
    parents = [Person(r.response) for r in req_parents]

    # Create family threads using recursion
    family_threads = [threading.Thread(target=depth_fs_pedigree, args=(p.parents, tree)) for p in parents if p is not None]
    # create children thread calling API to get the children data
    req_children = [Request_thread(f'{TOP_API_URL}/person/{id}') for id in children_ids]

    # Start all children threads
    for t in req_children:
        t.start()
    
    for person in parents:
        tree.add_person(person)
    
    # Start all family threads
    for thread in family_threads:
        thread.start()
    
    # Join all children threads
    for t in req_children:
        t.join()
    
    # Create the person
    for person in req_children:
        if person is not None:
            tree.add_person(Person(person.response))
    
    # Join Family threads so they call run concurently
    for thread in family_threads:
        thread.join()


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    tree_lock = threading.Lock()
    # Used internally.
    def get_family(family_id):
        """
        Fetches the family from id.
        Add family to tree.
        Put parents in current_parent_id_list
        put children in current_child_id_list
        """
        # Call Family API via thread
        req_family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
        req_family.start()
        req_family.join()
        
        # create a new family
        new_family = Family(family_id, req_family.response)
        
        # with tree_lock:
            # Add family to family tree
        tree.add_family(new_family)
        parents_ids = [new_family.husband, new_family.wife]
        current_parent_id_list.extend(parents_ids)
        children_ids = [c for c in new_family.children if not tree.does_person_exist(c)]
        current_child_id_list.extend(children_ids)

    def get_parent(id):
        """
        Fetch the person of the given id.
        Append the result's parents' family id to next_family_id_list
        Return the result person
        """
        # Call API via thread to get parent data
        req_person = Request_thread(f'{TOP_API_URL}/person/{id}')
        req_person.start()
        req_person.join()
        
        # Create parent
        new_person = Person(req_person.response)
        
        if new_person != None:
            # with tree_lock:
            # Add parent to family tree
            tree.add_person(new_person)
            return new_person.parents

    def get_child(id):
        """
        Fetch the person of the given id.
        Return the result person.
        """
        get_parent(id)

    current_family_id_list = [start_id]
    next_family_id_list = []
    
    while len(current_family_id_list) !=  0:
        current_parent_id_list = []
        current_child_id_list = []
        
        with ThreadPool(10) as pool:
            # Get family and collect parents, children
            pool.map(get_family, current_family_id_list)
            
            # print("got all the family pool")
            # print(f"parents: {current_parent_id_list}")
            # print(f"children: {current_child_id_list}")
            
            # Get parents and collect people, next generation family ids
            next_family_id_list = pool.map(get_parent, current_parent_id_list)
            
            # print(f"next family id list: {next_family_id_list}")
            
            # Get children and collect people
            pool.map(get_child, current_child_id_list)
        
        current_family_id_list = [id for id in next_family_id_list if id is not None]
        next_family_id_list = []


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # Limit number of threads running at one time to 5
    req_sem = threading.Semaphore(5)
    # Used internally.
    def get_family(family_id):
        """
        Fetches the family from id.
        Add family to tree.
        Put parents in current_parent_id_list
        put children in current_child_id_list
        """
        # Call Family API via thread
        req_family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
        
        with req_sem:
            # We are in a helper thread, so fetch without making a new thread.
            req_family.run()
        # create a new family
        new_family = Family(family_id, req_family.response)
        
        # Add family to family tree
        tree.add_family(new_family)
        parents_ids = [new_family.husband, new_family.wife]
        current_parent_id_list.extend(parents_ids)
        children_ids = [c for c in new_family.children if not tree.does_person_exist(c)]
        current_child_id_list.extend(children_ids)

    def get_parent(id):
        """
        Fetch the person of the given id.
        Append the result's parents' family id to next_family_id_list
        Return the result person
        """
        # Call API via thread to get parent data
        req_person = Request_thread(f'{TOP_API_URL}/person/{id}')
        
        with req_sem:
            # We are in a helper thread, so fetch without making a new thread
            req_person.run()
        
        # Create parent
        new_person = Person(req_person.response)
        
        if new_person != None:
            # Add parent to family tree
            tree.add_person(new_person)
            return new_person.parents

    def get_child(id):
        """
        Fetch the person of the given id.
        Return the result person.
        """
        get_parent(id)

    current_family_id_list = [start_id]
    next_family_id_list = []
    
    while len(current_family_id_list) !=  0:
        current_parent_id_list = []
        current_child_id_list = []
        
        with ThreadPool(10) as pool:
            # get family and collect parents, children
            pool.map(get_family, current_family_id_list)
            
            # print("got all the family pool")
            # print(f"parents: {current_parent_id_list}")
            # print(f"children: {current_child_id_list}")
            
            # get parents and collect people, next generation family ids
            next_family_id_list = pool.map(get_parent, current_parent_id_list)
            
            # print(f"next family id list: {next_family_id_list}")
            
            # get children and collect people
            pool.map(get_child, current_child_id_list)
        
        current_family_id_list = [id for id in next_family_id_list if id is not None]
        next_family_id_list = []

