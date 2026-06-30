int main(){
    int x, z;

    // pre-conditions
    x = 1;
    z = -1;

    // loop body
    while(unknown()){
        if(x < 0){
            z = 4 * z;
        }
        x = -(x + x);
        
    }

    // post-condition
    if(x > 5143523){
        assert((x + z) == 0);
    }
    
}