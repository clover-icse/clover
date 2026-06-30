int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 1000;
    z = 2000;
    

    // loop body
    while(unknown()){
        if(y >= 2000){
            z = z + 1;
        }
        if(x >= 1000){
            y = y + 1;
        }
        x = x + 1;
    }

    // post-condition
    if(y >= 2000){
        assert(x == z);
    }
    
}