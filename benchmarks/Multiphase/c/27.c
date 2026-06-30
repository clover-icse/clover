int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    assume(y >= 0);
    z = 0;

    // loop body
    while(unknown()){
        if(y == (x / 1000)){
            z = z + 1;
        }
        x = x + 1;
    }

    // post-condition
    if(x > (1000 * (y + 1))){
        assert(z == 1000);
    }
    
}