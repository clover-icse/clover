int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    assume(y >= 0);
    z = 0;

    // loop body
    while(unknown()){
        if(x >= (777 * y)){
            if(x < (777 * (5 + y))){
                z = z + 1;
            }
        }
        x = x + 1;
    }

    // post-condition
    if(x >= (777 * (10 + y))){
        assert(z == 3885);
    }
    
}