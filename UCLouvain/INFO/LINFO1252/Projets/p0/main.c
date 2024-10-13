#include<stdint.h>
#include<stdio.h>
#include<stddef.h>
#include<stdbool.h>

struct Metadata {
    struct Metadata* previous;
    struct Metadata* next;
    uint8_t* address; // Location of the data it's linked to
    uint16_t length;  // Length of the data it's linked to
    bool utilized;
};

uint8_t MY_HEAP[64000];

struct Metadata* separation;

struct Metadata* findDataPlace(){
    struct Metadata* ptr = ((struct Metadata*) (MY_HEAP+sizeof(MY_HEAP)))-1;
    while (ptr->utilized && ptr != separation){
        ptr--;
    }

    if(!ptr->utilized){
        ptr->utilized = true;
        return ptr;
    } else {
        struct Metadata new_data;
        new_data.utilized = true;
        separation--;
        ptr = separation;
        *ptr = new_data;
    }
    return ptr;
}

void init(){
    separation = ((struct Metadata*) (MY_HEAP+sizeof(MY_HEAP)))-1;

    // Initializing two dummy nodes
    struct Metadata new_data;
    new_data.previous = separation-1;
    new_data.next = separation-1;
    new_data.address = MY_HEAP;
    new_data.length = -1;
    new_data.utilized = true;
    *separation = new_data;

    separation--;
    new_data.previous = separation+1;
    new_data.next = separation+1;
    *separation = new_data;
}

void* my_malloc(size_t size){
    if (size == 0){
        return NULL;
    }
    
    struct Metadata* data = ((struct Metadata*) (MY_HEAP+sizeof(MY_HEAP)))-1;
    data = data->next;

    // Iterate until enough space found or reached the end of the data
    while (!(data->next->address - data->address - data->length >= size) && data->next->address != NULL){
        data = data->next;
    }

    // If reached the end of data
    if (data->next->address == NULL){
        // If there's enough space at the end of the data
        if ((void *) separation - (void *) data->address - data->length - sizeof(struct Metadata) > size){
            struct Metadata new_data;
            new_data.previous = data;
            new_data.next = data->next;
            new_data.address = 0;
            new_data.length = 0;
        }
    }


}

void my_free(void* pointer){
    return;
}

void main(){
    init();

    // Tests the dummy nodes
    // struct Metadata* ptr = separation;
    // printf("%p %p %p %i\n", ptr->previous, ptr->next, ptr->address, ptr->length);
    // ptr = ptr->next;
    // printf("%p %p %p %i\n", ptr->previous, ptr->next, ptr->address, ptr->length);
    // ptr = ptr->next;
    // printf("%p %p %p %i\n", ptr->previous, ptr->next, ptr->address, ptr->length);

    printf("%i\n", 0b1111111111111111);
}