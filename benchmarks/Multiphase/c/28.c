int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    assume(y >= 100);
    z = 0;

    // loop body
    while(unknown()){
        if(y <= (x / 50)){
            z = z + 1;
        }
        x = x + 1;
        y = y - 1;
    }

    // post-condition
    if(y == 0){
        assert(z > 0);
    }
    
}