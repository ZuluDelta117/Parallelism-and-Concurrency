    tree_lock = threading.Lock()
    #Used internally.
    def get_family(family_id):
        """
        Fetches the family from id.
        Add family to tree.
        Put parents in current_parent_id_list
        put children in current_child_id_list
        """
        req_pandemic = Request_thread(f'{TOP_API_URL}/family/{family_id}')
        # We are in a helper thread, so fetch without making a new thread.
        req_pandemic.start()
        req_pandemic.join()
        
        pandemic_data = req_pandemic.response
        virus1 = pandemic_data["virus1_id"]
        virus2 = pandemic_data["virus2_id"]
        offspring = retrieve_data_multiple(pandemic_data['offspring'])

        new_family = Family(family_id, virus1, virus2, offspring)
        with tree_lock:
            pandemic.add_family(new_family)
            parents_ids = [new_family.virus1, new_family.virus2]
            current_parent_id_list.extend(parents_ids)
            children_ids = [c for c in new_family.offspring if not pandemic.does_virus_exist(c)]
            current_child_id_list.extend(children_ids)

    def get_parent(id):
        """
        Fetch the person of the given id.
        Append the result's parents' family id to next_family_id_list
        Return the result person
        """
        req_virus = Request_thread(f'{TOP_API_URL}/virus/{id}')
        req_virus.start()
        req_virus.join()

        parent_data = req_virus.response
        print(f"parent data {parent_data}")
        virus_name = parent_data["name"]
        parent_id = parent_data["parent_id"]
        family_id = parent_data["family_id"]


        new_person = Virus(id, virus_name, parent_id, family_id)
        if new_person != None:
            with tree_lock:
                pandemic.add_virus(new_person)
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
        next_family_id_list = []

        # get family and collect parents, children
        for i in current_family_id_list:
            get_family(i)
        print("got all the family pool")
        print(f"parents: {current_parent_id_list}")
        print(f"children: {current_child_id_list}")
        # get parents and collect people, next generation family ids
        for i in current_parent_id_list:
            next_family_id_list.append(get_parent(i))
        print(f"next family id list: {next_family_id_list}")
        # get children and collect people

        for i in current_child_id_list:
            get_child(i)
        current_family_id_list = [id for id in next_family_id_list if id is not None]
        next_family_id_list = []