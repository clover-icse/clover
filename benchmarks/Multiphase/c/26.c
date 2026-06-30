int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    assume(y >= 25);
    z = 0;

    // loop body
    while(unknown()){
        if(y >= (x / 50)){
            z = z + 1;
        }
        x = 1 + x;
    }

    // post-condition
    if(x > (50 * y)){
        assert(z > 0);
    }
    
}