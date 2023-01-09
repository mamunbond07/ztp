
import logging
import copy
from mpi4py import MPI

class contract:
    """
    Handle a work queue on a contract for approved seekers
    """
   
    def __init__(self, master):
        #self.comm = MPI.COMM_WORLD
        self.master = master
        self.seeker = []
        self.keys   = []
        self.chunks = []
        self.work_queue           = []
        self.resources_work_queue = {}
        self.slave_resources      = {}
        self.node = 0


    def done(self):
        """
        Return True when there is no more work to do, the slaves are idle and
        get_completed_work has been called for all the completed slaves
        """
        return self.__work_queues_empty() and self.master.done()

    def add_work(self, data, node, resource_id=None):
        """
        Add more data to the work queue. When a slave become available this data
        will be passed to it
        """
        self.node = node
        self.__add_data(data, resource_id)
        #print("work-queue: ",node.id)
    '''
    Note: The do_work perfectly assign all the blocks to MULTIPLE nodes when total nodes >= 10 and fault_factor>=3
    '''
    def do_work(self):
        try:    
            if self.__work_queues_empty():
                return
        
            avail_slaves = []
            assigned = False 
            avail_slaves = self.master.get_ready_slaves()
            leader = 0
            fault_factor = 2 # Assumption of total faulty/byzantine nodes 
            while len(avail_slaves)>0:#=fault_factor-1:#2: # and not (self.__work_queues_empty()):#len(avail_slaves)>0:
                slave = avail_slaves.pop() 
            #############################################
            #If the cluster has few nodes, then work continues if at-least a leader exists 
            #############################################
                data, resource_id = self.__get_data_for_slave(slave)
            
                if data is None:
                    break    
            
                else:  #if slave in self.master.nodestatus:
                    self.slave_resources[slave] = resource_id
            
                
                #self.master.nodestatus[slave] is the status of a master, it is an integer value that holds total earned token of master 
                    '''
                    if slave in self.master.nodestatus and self.master.nodestatus[slave]>= 2 and len(avail_slaves)<=1:
                        data.nodes.append(slave)
                        self.master.run(slave, data)
                        print("Block",data.bid,"assigned to leader",slave, "Token ", self.master.nodestatus[slave])
                    '''

                    ''' 
                    if data.type == "response":
                        print("Only response check of block ",data.bid, "data nodes",data.nodes)
                    '''
                    #if data.type == "response" and slave not in data.nodes and slave in self.master.ready:
                    if data.type == "response" and  slave in self.master.ready: #slave in self.master.nodestatus:
                        #if len(avail_slaves)>0:
                        while len(data.response_handler) <= fault_factor and slave not in data.response_handler: # and len(avail_slaves)>0:# and slave in self.master.nodestatus:#and len(self.master.nodestatus)<=fault_factor : # and self.master.nodes[slave].type == "not-leader":
                        #self.master.nodes[slave].txn.append(data) 
                            data.response_handler.append(slave)
                            #print("Block",data.bid,"Assigned to a slave", slave, "has handlers ",data.response_handler)# "Token ",self.master.nodestatus[slave])
                            
                            self.master.run(slave,data)
                        
                            if len(avail_slaves)<=0: # and (len(data.nodes)>=fault_factor):
                                break
                            if (len(data.nodes)>=fault_factor):
                                break
                            slave = avail_slaves.pop()
                        #print("Block",data.bid, "has handlers ",data.response_handler)
                    elif data.type == "request"  and slave in self.master.ready:
                        data.nodes.append(slave)
                        self.master.run(slave,data)
                    '''
                    if len(data.nodes)<=fault_factor-2 and slave in self.master.nodestatus and self.master.nodestatus[slave]<=fault_factor-1:# and data.exceptions>3:
                        self.__add_data(data,None)
                        print("Block",data.bid, "is added back")
                    
                    #print("Slave is there ",slave, "token",self.master.nodestatus[slave], "Total validators ",len(data.nodes))
                    
                    if slave in self.master.nodestatus and self.master.nodestatus[slave]>= 1  and len(data.nodes)<=1:#len(avail_slaves)<=fault_factor-1:
                        data.nodes.append(slave)
                        self.master.run(slave, data)
                        print("Block",data.bid,"assigned to leader",slave, "Token ", self.master.nodestatus[slave])
                    '''
                    '''
                    if len(data.response_handler)<=1 and data.exceptions<=3: # and slave in self.master.ready:
                        print("Block",data.bid,"need more assignment")
                        print("Validators avaiable",len(avail_slaves))
                        #data.response_handler.append(slave)
                        #self.master.run(slave, data)
                        self.__add_data(data,None)
                        data.exceptions += 1
                    '''
                    '''
                    if slave in self.master.ready:
                        print("salve",slave, "is in ready list")
                    '''
        except Exception as ex:
            if len(data.nodes)<=fault_factor-2 and data.exceptions<=3:
                self.__add_data(data,None)
                data.exceptions += 1
                print("Block",data.bid, "is added back after exception")
            
            logging.error(logging.traceback.format_exc())
            print("Resource not available", ex)
            pass        


    def do_work2(self):
        """
        Assign data stored in the work queue to each idle slaves (if any)
        """

        if self.__work_queues_empty():
            return
        #print("master length workqueue: ",len(self.master.nodes))
        #
        # give work to do to each idle slave
        #
        for slave in self.master.get_ready_slaves():
           
            # get next task in the queue
            '''
            for obj in self.master.nodes:
                print("slave key: ", self.master.nodes[obj].id)
            
            if slave in self.master.nodes:   #checking availability of key in queue
                print(self.master.nodes[slave].id)
            '''
            data, resource_id = self.__get_data_for_slave(slave)
            
            if data is not None:
                #data.nodes.append(slave)
            
                if slave in self.master.nodes: 
                    #print(self.master.nodes[slave].id)
                    #self.master.nodes[slave].txn.append(data)
                    pass
                else: # The slave is not available in the master nodes list as ready states
                    self.node.id = slave
                    self.master.nodes[slave] = self.node
                    #print("Null k dorchi ",slave)
                #self.master.nodes[slave].txn.append(data) # In-memory txn storing. There should two queues: under-process txn & validated-txn
            
            #print("Nodes length: ",len(self.master.nodes), self.master.task, self.master.nodes[slave].id, data.id) # Helps in tracking if all nodes are properly holding data
            '''
            #####################
            The following code block will help in simulating/appending TXN/Node history in both TXN/NODE data structure.
            Note: We did not use this codeblock, as the READY queue is not implemented in NODE classes that holds individual READY NODES. READY queue is only implemented as INTEGER set
            ####################
            
            chk_slave = slave
            if chk_slave in self.master.nodes and self.master.nodes[slave] is not None and data is not None:   #checking availability of key in queue
                #k = (slave,self.master.nodes[slave])
                #print(type(self.master.nodes[slave]))
                #self.node.id = slave
                #self.node.type = self.master.nodes[slave].type
                data.nodes.append(slave) # Add the node as a processor of the Txn
                self.master.nodes[slave].txn.append(data) # Record the txn in the node
                print("resource-data",self.master.task, self.master.nodes[slave].id, data.id)
            
            else:
                print("master nodes list", len(self.master.nodes))
                print("Null Slave ",chk_slave)
            #data.nodes.append(slave)
            '''
            '''
            if data is not None and slave in self.master.nodes:
                self.master.nodes[slave].type = "not-leader"
                #data.nodes.append(self.node)
                print(self.master.nodes[slave].type)
            ''' 
                     
        
            if data is None:
                break

            # bind this slave to resource_id (that can be None)
            self.slave_resources[slave] = resource_id

            self.master.run(slave, data)
            #print(slave.type)
        
    def get_completed_work(self):
        """
        Fetch the return value of slave that completed its work
        """
        for slave in self.master.get_completed_slaves():
            yield self.master.get_data(slave)


    def __work_queues_empty(self):
        """
        Return True if all the work queues are empty. Some slaves might be still
        processing some data
        """
        return not self.work_queue and not self.resources_work_queue

    def __add_data(self, data, resource_id):
        if resource_id is None:
            # Anonymous work queue
            self.work_queue.append(data)
            #print("Anonymous Block ",data.bid)
        else:
            # add a task in the work queue with specifc resource_id
            work_queue = self.resources_work_queue.get(resource_id, list()) #Assign the job to a specific node
            work_queue.append(data)
            self.resources_work_queue[resource_id] = work_queue
            #print("Assigned to resource", resource_id)
            print("data added Block",data.bid)

    def __pop_data(self, resource_id):
        """
        Pop next task from the work queue with specifc resource_id
        """
        data = None
        if resource_id is None:
            # Anonymous work queue
            if self.work_queue:
                data = self.work_queue.pop(0)
        elif resource_id in self.resources_work_queue:
            # work queue with resource id
            work_queue = self.resources_work_queue[resource_id]
            data = work_queue.pop(0)
            if not work_queue:
                del self.resources_work_queue[resource_id]
        return data

    def __get_data_for_slave(self, slave):
        """
        Try to assign a resource to the same slave that processed it last time,
        This increase caching efficiency as the slave has already acquired the
        resource.
        Also this avoid that different slaves spend time acquiring the same
        resource: this is relevant when the resources are remote (database,
        network directory, etc) or, more generally, when acquiring/loading a
        resource takes time.
        """

        if self.__work_queues_empty():
            return None, None

        resources_to_process = set(self.resources_work_queue.keys())
        not_assigned_resources = resources_to_process - set(self.slave_resources.values())

        resource_id = self.slave_resources.get(slave)
        data = None

        #
        # Try to assign this slave to its previous resource if the slave has
        # a resource already assigned.
        #
        if resource_id is not None:
            data = self.__pop_data(resource_id)        

        #
        # Try to fetch next task from the work queue without resources
        #
        if data is None:
            resource_id = None
            data = self.__pop_data(resource_id)

        #
        # Try to assign this slave to a resource nobody else is using
        #        
        if data is None:
            if not_assigned_resources:
                resource_id = next(iter(not_assigned_resources))
                data = self.__pop_data(resource_id)

        #
        # Finally, assign this slave to a resource in use by other slaves
        #        
        if data is None:
            if resources_to_process:
                resource_id = next(iter(resources_to_process))
                data = self.__pop_data(resource_id)
        #print(data) 
        return data, resource_id
