int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 0;
    z = -1;

    // loop body
    while(unknown()){
        if(x % 2 == 0){
            z = z + 1;
        }
        x = x + 1;
        y = -(y + x);
    }

    // post-condition
    if(x == 942573485){
        assert((y + z) == 0);
    }
    
}