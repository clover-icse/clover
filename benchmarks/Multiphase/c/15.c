int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 0;
    z = 0;

    // loop body
    while(unknown()){
        if(x < 500){
            z = z + 2;
        }
        x = (x + 1) % 1000;
        y = y + 1;
        
    }

    // post-condition
    if(x == 0){
        assert(y == z);
    }
    
}