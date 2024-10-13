#include<stdint.h>
#include<stdio.h>
#include<stdlib.h>
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
    new_data.length = 0;
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
    
    // Starting at second dummy node
    struct Metadata* data = ((struct Metadata*) (MY_HEAP+sizeof(MY_HEAP)))-2;

    // Iterate until enough space found or reached the end of the data
    while (!(data->next->address - data->address - data->length >= size) && data->next->length != 0){
        data = data->next;
    }

    // If reached the end of data and not enough space
    if (data->next->length == 0 && (void *) separation - (void *) data->address - data->length - sizeof(struct Metadata) < size){
        printf("Not enough space !\n");
        return (void *) NULL;
    }

    // In any other case, adjusting pointers and creating new meta-data for the new block
    struct Metadata* new_data = findDataPlace();

    // adjusting pointers
    new_data->previous = data;
    new_data->next = data->next;
    new_data->next->previous = new_data;
    data->next = new_data;

    // Setting up new meta-data
    new_data->address = data->address+data->length;
    new_data->length = size;
    new_data->utilized = true;
    return new_data->address;
}

void my_free(void* pointer){
    struct Metadata* data = ((struct Metadata*) (MY_HEAP+sizeof(MY_HEAP)))-2;
    while (data->next->length != 0){
        data = data->next;
        if (data->address == pointer){
            data->utilized = false;
            data->previous->next = data->next;
            data->next->previous = data->previous;
            return;
        }
    }
}

void print_metadata(){
    printf("PRINTING METADATA : \n");
    int nel = 0;
    struct Metadata* data = ((struct Metadata*) (MY_HEAP+sizeof(MY_HEAP)))-2;
    while (data->next->length != 0){
        data = data->next;
        printf("previous : %p   current : %p   next : %p   address : %p    length : %u    utilized : %i\n", data->previous, data, data->next, data->address, data->length, data->utilized);
        nel++;
    }
    printf("Total blocks : %i\n\n", nel);
}

void main(){
    init();
    printf("HEAP starting at %p and ending at %p\n\n", MY_HEAP, MY_HEAP+sizeof(MY_HEAP));

    // DUMMY NODES TEST
    // struct Metadata* ptr = separation;
    // printf("%p %p %p %i\n", ptr->previous, ptr->next, ptr->address, ptr->length);
    // ptr = ptr->next;
    // printf("%p %p %p %i\n", ptr->previous, ptr->next, ptr->address, ptr->length);
    // ptr = ptr->next;
    // printf("%p %p %p %i\n", ptr->previous, ptr->next, ptr->address, ptr->length);

    // INT ARRAY TEST
    // int* new_array = my_malloc(sizeof(int)*6);

    // for (int i = 0; i < 6; i++){
    //     *new_array = i;
    //     new_array++;
    // }
    // print_metadata();

    // int* ptr = (int*) MY_HEAP;
    // for (int i = 0; i < 6; i++){
    //     printf("%u", *ptr);
    //     ptr++;
    // }
    // printf("\n");


    // MALLOC AND FREE TEST
    int* array;
    do{
        array = my_malloc(2048);
    } while (array != NULL);
    print_metadata();
}