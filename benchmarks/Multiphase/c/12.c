int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 0;
    z = 0;

    // loop body
    while(unknown()){
        if(x % 2 == 0){
            y = y + 1;
        }else{
            z = z + 1;
        }
        x = x + 1;
    }

    // post-condition
    if(x == 1342342){
        assert(y == z);
    }
    
}